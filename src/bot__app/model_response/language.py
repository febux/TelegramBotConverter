from typing import Optional

from src.utils.api_utils.internal_api import JsonApiPayload


class ApiLanguageResponse(JsonApiPayload):
    language_abbr: str
    language_name: Optional[str]
