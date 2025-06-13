from abc import ABC, abstractmethod
from typing import Any

class MultiSetInterface(ABC):

    def __init__(self):
        self._multiset = dict()

    def __repr__(self):
        return f'{self.__class__.__name__}: {str(self._multiset)}'
    
    def __and__(self, other: 'MultiSetInterface'):
        if not isinstance(other, MultiSetInterface):
            return NotImplemented
        
        keys = set(self.multiset.keys()) & set(other.multiset.keys())

        obj = self.__class__()
        for key in keys:
            m_self = self.multiset[key]
            m_other = other.multiset[key]
            m = min(m_self, m_other)
            if m > 0:
                obj.add(key, m)
        return obj

    @property
    def multiset(self):
        return self._multiset

    @multiset.setter
    def multiset(self, multiset):
        self._multiset = multiset

    def items(self):
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
    def sub(self, obj: Any, multiplicity: int) -> bool:
        pass

    @abstractmethod
    def remove(self, obj: Any, multiplicity: int) -> bool:
        pass