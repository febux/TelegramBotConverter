import abc
from typing import List
from uuid import UUID

from src.bot__db.models.base_model import BaseModel


class AbstractRepository(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def add(cls):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get(cls, identifier: UUID) -> BaseModel:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_all(cls) -> List[BaseModel]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update(cls, identifier: UUID) -> BaseModel:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete(cls, identifier: UUID) -> None:
        raise NotImplementedError
