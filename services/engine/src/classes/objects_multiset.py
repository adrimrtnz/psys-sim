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

    def count_subsets(self):
        return len(self.multiset.keys())

    def is_empty(self):
        return self.count_subsets() == 0

    def remove(self, obj: str, multiplicity: int = 1) -> bool:
        if obj is None:
            raise ValueError("ObjectsMultiset.remove -> object cannot be null")
        if multiplicity < 0:
            raise ValueError("ObjectsMultiset.remove -> object multiplicity cannot be negative")
        if multiplicity == 0:
            return False
        current_multiplicity = self.multiset.get(obj, None)
        if current_multiplicity is None:
            return False
        if current_multiplicity < multiplicity:
            return False
        if current_multiplicity == multiplicity:
            del self.multiset[obj]
        else:
            self.multiset[obj] = self.multiset.get(obj, 0) - multiplicity
        return True

    def remove_all(self):
        self.multiset = dict()
