from abc import ABC, abstractmethod
from typing import Any

class MultiSetInterface(ABC):

    def __init__(self):
        self._multiset = dict()

    @property
    def multiset(self):
        return self._multiset

    @multiset.setter
    def multiset(self, multiset):
        self._multiset = multiset

    def get_all(self):
        return self.multiset.items()

    @abstractmethod
    def count(self, _object):
        pass

    @abstractmethod
    def count_subsets(self, objects):
        pass

    @abstractmethod
    def add(self, obj: Any, multiplicity: int) -> bool:
        pass

    @abstractmethod
    def remove(self, obj: Any, multiplicity: int) -> bool:
        pass