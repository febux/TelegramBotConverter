import os

from src.utils.api_utils.internal_api import InternalApi


internal_api = InternalApi(flask_app_name='internal_api_flask_app', entry_point=os.environ['INTERNAL_API_ENDPOINT'])
