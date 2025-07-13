from src.interfaces.multiset_interface import MultiSetInterface

class ObjectsMultiset(MultiSetInterface):

    def add(self, obj: str, multiplicity: int = 1) -> bool:
        if obj is None:
            raise ValueError("ObjectsMultiset.add -> object cannot be null")
        if multiplicity < 0:
            raise ValueError("ObjectsMultiset.add -> object multiplicity cannot be negative")
        if multiplicity == 0:
            return False
        self.multiset[obj] = self.multiset.get(obj, 0) + multiplicity
        return True

    def sub(self, obj: str, multiplicity: int = 1) -> bool:
        if obj is None:
            raise ValueError("ObjectsMultiset.sub -> object cannot be null")
        if multiplicity < 0:
            raise ValueError("ObjectsMultiset.sub -> object multiplicity cannot be negative")
        if multiplicity == 0:
            return False

        count = self.multiset.get(obj, 0)
        if count < multiplicity:
            return False
        self.multiset[obj] = self.multiset.get(obj, 0) - multiplicity
        if self.multiset[obj] == 0:
            del self.multiset[obj]
        return True

    def contains(self, _object) -> bool:
        value = self.count(_object)
        return value > 0

    def count(self, _object):
        return self._multiset.get(_object, 0)

    def count_subsets(self, other):
        """
        Count how many times the ObjectMultiset 'other' is included in self.
        
        Args:
            other
        
        Returns:
            int: number of times that self contains other
        """
        if not isinstance(other, self.__class__):
            return 0
        
        # If other.multiset is empty, it is technically included infinitely many times.
        if not other.multiset:
            return float('inf')
            
        min_quotient = float('inf')
    
        for obj, mult in other._multiset.items():
            self_count = self._multiset.get(obj, 0)
            if self_count == 0:
                return 0
            
            quotient = self_count // mult
            min_quotient = min(min_quotient, quotient)
            
            # If it is already 0, stop and return
            if min_quotient == 0:
                return 0
        
        return min_quotient

    def is_empty(self):
        return len(self.multiset.keys()) == 0

    def remove(self, obj: str) -> bool:
        if obj is None:
            raise ValueError("ObjectsMultiset.remove -> object cannot be null")
        
        current_multiplicity = self.multiset.get(obj, None)
        if current_multiplicity is None:
            return False

        del self.multiset[obj]
        return True

    def remove_all(self):
        self.multiset = dict()
