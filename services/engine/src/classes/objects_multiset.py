from src.interfaces.multiset_interface import MultiSetInterface

class ObjectsMultiset(MultiSetInterface):

    def count(self, _object):
        return self._multiset.get(_object, 0)

    def count_subsets(self):
        return len(self._multiset.keys())

    def add(self, obj: str, multiplicity: int) -> bool:
        if obj is None:
            raise ValueError("ObjectsMultiset.add -> object cannot be null")
        if multiplicity < 0:
            raise ValueError("ObjectsMultiset.add -> object multiplicity cannot be negative")
        if multiplicity == 0:
            return False
        self._multiset[obj] = self._multiset.get(obj, 0) + multiplicity
        return True

    def remove(self, obj: str, multiplicity: int) -> bool:
        if obj is None:
            raise ValueError("ObjectsMultiset.remove -> object cannot be null")
        if multiplicity < 0:
            raise ValueError("ObjectsMultiset.remove -> object multiplicity cannot be negative")
        if multiplicity == 0:
            return False
        current_multiplicity = self._multiset.get(obj, None)
        if current_multiplicity is None:
            return False
        if current_multiplicity < multiplicity:
            # TODO: Preguntar si esto es así o se dejaría el objeto a multiplicidad=0
            return False
        if current_multiplicity == multiplicity:
            del self._multiset[obj]
        else:
            self._multiset[obj] = self._multiset.get(obj, 0) - multiplicity
        return True