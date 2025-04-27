from typing import List

class MembraneObject:
    def __init__(self, v: str, m: int):
        self._v = v
        self._m = m

    def __str__(self):
        return f'OB - (v={self.value}, mul={self.multiplicity})'

    @property
    def value(self):
        return self._v
    
    @property
    def multiplicity(self):
        return self._m
    

class Membrane:
    def __init__(self, idx: str, m: int, capacity: int, parent: 'Membrane' = None):
        self._id = idx
        self._m = m
        self._cap = capacity
        self._parent = parent
        self._children = []
        self._objects = []

    def __str__(self):
        return f'Membrane - (id={self.id}, mul={self.multiplicity}, capacity={self.capacity})'

    @property
    def id(self):
        return self._id
    
    @property
    def multiplicity(self):
        return self._m
    
    @property
    def capacity(self):
        return self._cap
    
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return self._children
    
    @property
    def objects(self):
        return self._objects
    
    def add_children(self, value: List['Membrane'] | 'Membrane'):
        """
        Function to add children to the Membrane

        Args:
            value: Membrane or list of Membranes
        """
        if type(value) is list:
            if all(isinstance(v, Membrane) for v in value):
                self._children.extend(value)
            else:
                raise ValueError('All the children to add should be an instance of Membrane')
        elif isinstance(value, Membrane):
            self._children.append(value)


    def add_objects(self, value: List[MembraneObject] | MembraneObject):
        """
        Function to add objects to the Membrane

        Args:
            value: MembraneObject or list of MembraneObject
        """
        if type(value) is list:
            if all(isinstance(v, MembraneObject) for v in value):
                self._objects.extend(value)
            else:
                raise ValueError('All the objects to add should be an instance of MembraneObject')
        elif isinstance(value, MembraneObject):
            self._objects.append(value)

    def print_structure(self, level=0):
        print(f'{"   " * level}{str(self)}')
        for ob in self.objects:
            print(f'{"   " * level}  {str(ob)}')

        for child in self.children:
            child.print_structure(level + 1)