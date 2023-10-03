from abc import ABC, abstractmethod

class AbstractSession(ABC):

    @abstractmethod
    def get_session():
        raise NotImplementedError()

