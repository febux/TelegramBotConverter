from typing import Dict, List


class AbstractApiError(Exception):
    pass


class AbstractInternalApiError(AbstractApiError):
    pass


class RequestAbstractInternalApiError(AbstractApiError):
    def __init__(self, message: str, error: Exception) -> None:
        assert isinstance(message, str), f'message must be str. "{type(message).__name__}" was given'
        assert isinstance(error, Exception), f'error must be Exception. "{type(error).__name__}" was given'
        super(RequestAbstractInternalApiError, self).__init__(f'{message} :: {error}')
        self.error = error


class NotFinishedRequestInternalApiError(RequestAbstractInternalApiError):
    pass


class ResponseAbstractInternalApiError(AbstractInternalApiError):
    pass


class NotCheckedResponseInternalApiError(ResponseAbstractInternalApiError):
    pass


class ResponseFormatInternalApiError(ResponseAbstractInternalApiError):
    pass


class ResponseDataAbstractInternalApiError(ResponseAbstractInternalApiError):
    def __init__(self, message: str, error: Exception) -> None:
        assert isinstance(message, str), f'message must be str. "{type(message).__name__}" was given'
        assert isinstance(error, Exception), f'error must be Exception. "{type(error).__name__}" was given'
        super(ResponseDataAbstractInternalApiError, self).__init__(f'{message} :: {error}')
        self.error = error


class ResponseJsonInternalApiError(ResponseDataAbstractInternalApiError):
    pass


class ResponseJsonSchemaInternalApiError(ResponseDataAbstractInternalApiError):
    pass


class ResponsePayloadTypeInternalApiError(ResponseDataAbstractInternalApiError):
    pass


class InternalApiResponseErrorObj(ResponseDataAbstractInternalApiError):
    pass


class ResponseStatusAbstractInternalApiError(ResponseAbstractInternalApiError):

    def __init__(self, status_code: int, errors: List[InternalApiResponseErrorObj]) -> None:
        assert isinstance(status_code, int), f'status_code must be int. "{type(status_code).__name__}" was given'
        assert status_code >= 400
        super(ResponseStatusAbstractInternalApiError, self).__init__(f'status code error :: {status_code} :: {errors}')
        self.status_code = status_code
        self.errors = errors


class Server5XXInternalApiError(ResponseStatusAbstractInternalApiError):
    def __init__(self, status_code: int, errors: List[InternalApiResponseErrorObj]) -> None:
        assert 500 <= status_code
        super(Server5XXInternalApiError, self).__init__(status_code, errors)


class Client4XXInternalApiError(ResponseStatusAbstractInternalApiError):
    def __init__(self, status_code: int, errors: List[InternalApiResponseErrorObj]) -> None:
        assert 400 <= status_code < 500
        super(Client4XXInternalApiError, self).__init__(status_code, errors)


class UserAbstractApiError(AbstractApiError):
    pass


class ValidationListApiError(UserAbstractApiError):
    def __init__(self, errors: List[Dict[str, str]]):
        super().__init__(f'validation errors: {errors}')
        self.errors = errors


class ValidateApiError(UserAbstractApiError):
    code = "{code}"
    location = ["{location}"]
    msg_template = "{msg_template}"


class SimpleValidateApiError(UserAbstractApiError):
    pass


class AccessApiError(UserAbstractApiError):
    pass


class PermissionDeniedApiError(UserAbstractApiError):
    pass


class NoResultFoundApiError(UserAbstractApiError):
    pass


class HasAlreadyExistsApiError(UserAbstractApiError):
    pass


class InvalidContentTypeError(UserAbstractApiError):
    pass


class RuntimeAbstractApiError(AbstractApiError):
    pass


class ResourceRuntimeApiError(RuntimeAbstractApiError):
    pass


class ResponseTypeRuntimeApiError(RuntimeAbstractApiError):
    pass


class WrapInternalApiError(Exception):

    def __init__(self, message: str, error: AbstractInternalApiError) -> None:
        super().__init__(message)
        self.error = error
