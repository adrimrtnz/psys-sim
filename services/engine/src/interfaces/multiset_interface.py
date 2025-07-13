from abc import ABC, abstractmethod
from typing import Any

"""
MultiSet interface module for membrane computing systems.

This module provides an abstract base class that defines the interface
for multiset operations used in membrane computing simulations.
"""

class MultiSetInterface(ABC):
    """Abstract base class for multiset implementations.
    
    This class provides a common interface for multiset data structures,
    which are collections that allow multiple occurrences of elements.
    It includes set operations like intersection and union, as well as
    abstract methods that must be implemented by subclasses.
    
    The multiset is internally represented as a dictionary where keys are
    objects and values are their multiplicities (counts).
    
    Attributes:
        multiset (dict): Dictionary storing objects and their counts.
    """

    def __init__(self):
        """Initialize an empty multiset.
        
        Creates a new multiset instance with an empty internal dictionary.
        """
        self._multiset = dict()

    def __repr__(self):
        """Return string representation of the multiset.
        
        Returns:
            str: String showing the class name and multiset contents.
        """
        return f'{self.__class__.__name__}: {str(self._multiset)}'
    
    def __and__(self, other: 'MultiSetInterface'):
        """Compute intersection of two multisets.
        
        The intersection contains elements that appear in both multisets,
        with multiplicity equal to the minimum count in either multiset.
        
        Args:
            other (MultiSetInterface): Another multiset to intersect with.
            
        Returns:
            MultiSetInterface: New multiset containing the intersection.
            NotImplemented: If other is not a MultiSetInterface instance.
        """
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
    
    def __or__(self, other: 'MultiSetInterface'):
        """Compute union of two multisets.
        
        The union contains all elements from both multisets, with
        multiplicity equal to the maximum count in either multiset.
        
        Args:
            other (MultiSetInterface): Another multiset to unite with.
            
        Returns:
            MultiSetInterface: New multiset containing the union.
            NotImplemented: If other is not a MultiSetInterface instance.
        """
        if not isinstance(other, MultiSetInterface):
            return NotImplemented
        
        keys = set(self.multiset.keys()) | set(other.multiset.keys())

        obj = self.__class__()
        for key in keys:
            m_self = self.multiset.get(key, 0)
            m_other = other.multiset.get(key, 0)
            m = max(m_self, m_other)
            if m > 0:
                obj.add(key, m)
        return obj
    
    def __add__(self, other: 'MultiSetInterface'):
        """Compute the sum of two multisets.
        
        Args:
            other (MultiSetInterface): Another multiset to sum with.
            
        Returns:
            MultiSetInterface: New multiset containing the union.
            NotImplemented: If other is not a MultiSetInterface instance.
        """
        keys = set(self.multiset.keys()) | set(other.multiset.keys())

        obj = self.__class__()
        for key in keys:
            m_self = self.multiset.get(key, 0)
            m_other = other.multiset.get(key, 0)
            obj.add(key, m_self + m_other)
        return obj

    @property
    def multiset(self):
        """Get the internal multiset dictionary."""
        return self._multiset

    @multiset.setter
    def multiset(self, multiset):
        """Set the internal multiset dictionary.

        Args:
            multiset (dict): Dictionary to set as the internal multiset.
        """
        self._multiset = multiset

    def items(self):
        """Get items from the multiset.
        
        Returns:
            dict_items: Key-value pairs from the internal multiset dictionary.
        """
        return self.multiset.items()

    @abstractmethod
    def count(self, _object):
        """Count occurrences of an object in the multiset.
        
        Args:
            _object: Object to count in the multiset.
            
        Returns:
            int: Number of occurrences of the object.
        """
        pass

    @abstractmethod
    def count_subsets(self, objects):
        pass

    @abstractmethod
    def add(self, obj: Any, multiplicity: int) -> bool:
        """Add objects to the multiset.
        
        Args:
            obj (Any): Object to add to the multiset.
            multiplicity (int): Number of copies to add.
            
        Returns:
            bool: True if addition was successful, False otherwise.
        """
        pass

    @abstractmethod
    def sub(self, obj: Any, multiplicity: int) -> bool:
        """Subtract objects from the multiset.
        
        Args:
            obj (Any): Object to subtract from the multiset.
            multiplicity (int): Number of copies to subtract.
            
        Returns:
            bool: True if subtraction was successful, False otherwise.
        """
        pass

    @abstractmethod
    def remove(self, obj: Any) -> bool:
        """Remove objects from the multiset.
        
        Args:
            obj (Any): Object to remove from the multiset.
            
        Returns:
            bool: True if removal was successful, False otherwise.
        """
        pass