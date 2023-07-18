import logging
import time
import urllib.parse
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, TypeVar, List
import requests
from flask import g as ctx
from pydantic import BaseModel, Extra, UUID4
# from src.internal_api.app import internal_api_flask_app
from werkzeug.datastructures import FileStorage

from src.utils.api_utils.api_format import ApiFormat
from src.utils.api_utils.const import REQUEST_HEADER__CONTENT_TYPE
from src.utils.api_utils.errors import NotFinishedRequestInternalApiError


logging.getLogger(__name__)


class JsonApiPayloadType(BaseModel):
    class Config:
        extra = Extra.ignore


class JsonApiPayload(JsonApiPayloadType):
    identifier: UUID4

    created_at: datetime
    updated_at: datetime


TPayloadType = TypeVar('TPayloadType', bound=List[JsonApiPayloadType] | JsonApiPayloadType | None)


# @internal_api_flask_app.teardown_appcontext
# def teardown_session(exception):
#     session = ctx.pop('internal_api_requests_session', None)
#
#     if session is not None:
#         session.close()


def get_or_create_session(testing_mode: bool) -> requests.Session:
    if testing_mode:
        if getattr(ctx, 'internal_api_requests_session', None) is None:
            return requests.Session()
    if 'internal_api_requests_session' not in ctx:
        ctx.internal_api_requests_session = requests.Session()
    return ctx.internal_api_requests_session


internal_api_registry: Dict[str, 'InternalApi'] = {}


def cleanup_q(query: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if query is None:
        return None
    res = {}
    for k, v in query.items():
        if v is not None:
            res[k] = v
    return res


class ApiMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'

    def __str__(self):
        return self.value


NO_REQUEST_BODY_METHODS = {ApiMethod.GET, ApiMethod.OPTIONS}


class InternalApi:

    def __init__(
            self,
            flask_app_name: str,
            entry_point: str,
            *,
            auth_method: str = 'Bearer',
    ) -> None:
        r = urllib.parse.urlparse(entry_point)
        has_path_pref_in_entry_point = not (r.path == '' or r.path == '/')
        assert r.query == ''
        assert r.fragment == ''
        assert r.scheme in {'http', 'https'}
        self._flask_app_name = flask_app_name
        self._entry_point = urllib.parse.urlunparse(r._replace(path=''))
        self._auth_method = auth_method
        internal_api_registry[self._entry_point] = self
        self._testing_mode = False

    @property
    def entry_point(self) -> str:
        return self._entry_point

    def request_get(
            self,
            path: str,
            *,
            q: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            payload_type: Optional[TPayloadType] = None,
    ) -> Dict[str, Any] | TPayloadType:
        if payload_type:
            response = self.request(
                ApiMethod.GET,
                path,
                q=q,
                headers=headers,
            ).json()
            if isinstance(response, list):
                return [payload_type(**res) for res in response]     # noqa
            elif isinstance(response, dict):
                return payload_type(**response)     # noqa
        return self.request(
            ApiMethod.GET,
            path,
            q=q,
            headers=headers,
        ).json()

    def request_post(
            self,
            path: str,
            *,
            q: Optional[Dict[str, Any]] = None,
            json: Optional[Any] = None,
            files: Optional[Dict[str, FileStorage]] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        return self.request(
            ApiMethod.POST,
            path,
            q=q,
            json=json,
            files=files,
            headers=headers,
        )

    def request_patch(
            self,
            path: str,
            *,
            q: Optional[Dict[str, Any]] = None,
            json: Optional[Any] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        return self.request(
            ApiMethod.PATCH,
            path,
            q=q,
            json=json,
            headers=headers,
        )

    def request_delete(
            self,
            path: str,
            *,
            q: Optional[Dict[str, Any]] = None,
            json: Optional[Any] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        return self.request(
            ApiMethod.DELETE,
            path,
            q=q,
            json=json,
            headers=headers,
        )

    def request_put(
            self,
            path: str,
            *,
            q: Optional[Dict[str, Any]] = None,
            json: Optional[Any] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        return self.request(
            ApiMethod.PUT,
            path,
            q=q,
            json=json,
            headers=headers,
        )

    def request(
            self,
            method: ApiMethod,
            path: str,
            *,
            q: Optional[Dict[str, Any]] = None,
            json: Optional[Any] = None,
            files: Optional[Dict[str, FileStorage]] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        assert isinstance(method, ApiMethod), f'method must be ApiMethod. "{type(method).name}" was given'

        started_at = time.time()
        q = cleanup_q(q)
        url = f'{self._entry_point.rstrip("/")}{path}'

        req_headers = {}

        req_headers.update(headers or {})

        data = json

        if json is not None:
            assert method not in NO_REQUEST_BODY_METHODS, f'{method.value} {url} :: must have no body'

            content_type = ApiFormat.JSON
            data = content_type.serialize_bytes(json)

            req_headers[REQUEST_HEADER__CONTENT_TYPE] = content_type.mime

        try:
            requests_response = get_or_create_session(self._testing_mode).request(
                method.value,
                url=url,
                files=({name: (fs.filename, fs.stream, fs.content_type, fs.headers) for name, fs in files.items()}
                       if files is not None else None),
                headers=req_headers,
                data=data,
                params=q,
            )
        except Exception as error:  # noqa: B902
            raise NotFinishedRequestInternalApiError('request not finished', error)
        return requests_response
