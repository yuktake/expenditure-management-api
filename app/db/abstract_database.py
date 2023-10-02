from abc import ABC, abstractmethod
from typing import Callable
from contextlib import contextmanager, AbstractContextManager
from sqlalchemy.orm import Session

class AbstractDatabase(ABC):
    def create_database(self) -> None:
        raise NotImplementedError()

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        raise NotImplementedError()