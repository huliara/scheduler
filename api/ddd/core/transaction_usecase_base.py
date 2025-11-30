from abc import abstractmethod
from typing import Any

from database import Base
from ddd.core.usecase_base import UseCaseBase


class TransactionUseCaseBase(UseCaseBase):

    @abstractmethod
    def _transaction(self, *args: Any, **kwargs: Any) -> Base:
        pass
