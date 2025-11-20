from abc import abstractmethod
from typing import Any

from sqlalchemy.orm import Session

from app.database import Base
from app.ddd.core.usecase_base import UseCaseBase


class TransactionUseCaseBase(UseCaseBase):

    @abstractmethod
    def _transaction(self, *args: Any, **kwargs: Any) -> Base:
        pass
