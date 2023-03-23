from abc import ABC, abstractmethod

class PasswordService(ABC):
    @abstractmethod
    def hash(self, raw: str) -> str:
        pass

    @abstractmethod
    def valid(self, raw: str, hashed: str) -> bool:
        pass

