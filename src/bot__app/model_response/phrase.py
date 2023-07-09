from typing import Optional

from src.utils.api_utils.internal_api import JsonApiPayload


class ApiPhraseResponse(JsonApiPayload):
    phrase_key: str
    description: Optional[str]
