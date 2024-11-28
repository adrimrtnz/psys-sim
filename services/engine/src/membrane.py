class Membrane:
    def __init__(self, id: str, m: int, parent: 'Membrane' = None):
        self._id = id
        self._m = m
        self._parent = parent
        self._objects = []

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    @property
    def multiplicity(self):
        return self._m


class MembraneObject:
    def __init__(self, v: str, m: int):
        self._v = v
        self._m = m

    @property
    def value(self):
        return self._v
    
    @property
    def multiplicity(self):
        return self._m
    