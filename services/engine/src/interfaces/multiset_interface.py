from abc import ABC, abstractmethod


class MultiSetInterface(ABC):

    def __init__(self):
        self._multiset = dict()

    def get_all(self):
        return self._multiset.items()

    @abstractmethod
    def count(self, _object):
        pass

    @abstractmethod
    def count_subsets(self, objects):
        pass

    @abstractmethod
    def add(self, _object, multiplicity) -> bool:
        pass

    @abstractmethod
    def remove(self, _object, multiplicity) -> bool:
        pass