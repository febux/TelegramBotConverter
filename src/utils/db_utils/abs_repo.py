import abc
from uuid import UUID

from src.bot__db.models.base_model import BaseModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, identifier: UUID) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, identifier: UUID) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, identifier: UUID) -> None:
        raise NotImplementedError
