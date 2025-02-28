class Membrane:
    def __init__(self, id: str, m: int, parent: 'Membrane' = None):
        self._id = id
        self._m = m
        self._parent = parent
        self._children = []
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
    
    def add_children(self, value):
        """
        Function to add children to the Membrane

        Args:
            value: Membrane or list of Membranes
        """
        if type(value) is list and all(isinstance(value, Membrane)):
            self._children.extend(value)
        elif isinstance(value, Membrane):
            self._children.append(value)


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
    