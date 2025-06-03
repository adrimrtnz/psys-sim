from typing import List
from src.classes.membrane_object import MembraneObject
from src.classes.objects_multiset import ObjectsMultiset


class Membrane:
    def __init__(self, idx: str, multiplicity : int, capacity: int, parent: 'Membrane' = None):
        self._id = idx
        self._m = multiplicity
        self._cap = capacity
        self._parent = parent
        self._children = []
        self._objects = ObjectsMultiset()

        self._alive = True
        self._step = 0

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


    def add_objects(self, objects: List[MembraneObject] | MembraneObject) -> bool:
        """
        Function to add objects to the Membrane

        Args:
            objects: MembraneObject or list of MembraneObject
        """
        if type(objects) is list:
            for _object in objects:
                if isinstance(_object, MembraneObject):
                    self._objects.add(_object.value, int(_object.multiplicity))
                else:
                    raise ValueError('All the objects to add should be an instance of MembraneObject')
        elif isinstance(objects, MembraneObject):
            self._objects.add(objects.value, int(objects.multiplicity))
        return True

    def print_structure(self, level=0):
        print(f'{"   " * level}{str(self)}')
        for key, value in self.objects.get_all():
            print(f'{"   " * level}  OB - (v={key}, mul={value})')

        for child in self.children:
            child.print_structure(level + 1)