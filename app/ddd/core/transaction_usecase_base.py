from abc import abstractmethod
from typing import Any

from sqlalchemy.orm import Session

from app.database import Base
from app.ddd.core.usecase_base import UseCaseBase


class TransactionUseCaseBase(UseCaseBase):

    def __init__(self, db: Session) -> None:
        self._db: Session = db

    @abstractmethod
    def _transaction(self, *args: Any, **kwargs: Any) -> Base:
        pass

    def db(self) -> Session:
        return self._db