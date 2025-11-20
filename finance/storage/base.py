from abc import ABC, abstractmethod
from typing import List
from finance.models.schemas import Transaction

class IStorage(ABC):
    @abstractmethod
    def get_all(self) -> List[Transaction]:
        pass

    @abstractmethod
    def append(self, transaction: Transaction):
        pass