from pydantic import UUID4

from src.bot__app.model_response.language import ApiLanguageResponse
from src.bot__app.model_response.phrase import ApiPhraseResponse
from src.utils.api_utils.internal_api import JsonApiPayload


class ApiTranslationResponse(JsonApiPayload):
    phrase_id: UUID4
    phrase: ApiPhraseResponse

    language_id: UUID4
    language: ApiLanguageResponse

    translation_content: str
