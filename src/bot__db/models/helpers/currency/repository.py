from typing import Dict, Any, List
from uuid import UUID

from src.bot__db import Currency
# from src.bot__db.app import db_flask_app
from src.bot__db.models.base_model import BaseModel
from src.utils.db_utils.abs_repo import AbstractRepository
from src.utils.db_utils.db_app_context import db_app_context


class CurrencyRepository(AbstractRepository):
    model = Currency

    @classmethod
    def add(cls):
        pass

    @classmethod
    def get(cls, identifier: UUID) -> BaseModel:
        pass

    @classmethod
    @db_app_context
    def get_all(cls) -> List[Dict[str, Any]]:
        result = cls.model.query.all()
        return [obj.to_dict() for obj in result]

    @classmethod
    def update(cls, identifier: UUID) -> BaseModel:
        pass

    @classmethod
    def delete(cls, identifier: UUID) -> None:
        pass
