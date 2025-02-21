from collections.abc import Callable
from typing import Any

from app.ddd.core.exception import DomainException, UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase


def transaction(func: Callable[..., Any]) -> Callable[..., Any]:

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        usecase: TransactionUseCaseBase = args[0]
        try:
            result = func(*args, **kwargs)
        except DomainException:
            usecase.db().rollback()
            raise
        except Exception as e:
            usecase.db().rollback()
            raise UseCaseException(description=f"{e}") from e
        else:
            usecase.db().commit()
        return result

    return wrapper