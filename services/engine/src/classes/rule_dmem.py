from typing import List, Union, Dict
from src.enums.constants import MoveCode
from src.classes.rule import Rule
from src.classes.objects_multiset import ObjectsMultiset

"""
Rule module for membrane computing systems.

This module defines the Rule class which represents transformation rules
in P-Systems. Rules define how objects are consumed and produced within
membranes, along with their movement patterns and execution probabilities.
"""

class RuleDMEM(Rule):
    """Represents a transformation rule in a P-System membrane.
    
    A rule defines a transformation from a left-hand side (consumed objects)
    to a right-hand side (produced objects), along with movement instructions,
    probabilities, and priorities that control its application.
    
    Attributes:
        left (ObjectsMultiset): Objects consumed by the rule (left-hand side).
        right (ObjectsMultiset): Objects produced by the rule (right-hand side).
        probability (float): Probability of applying the rule when applicable.
        priority (Union[List[str], None]): List of rule IDs that have priority over this rule.
        move (str): Movement code defining where the produced objects are sent.
        destination (Union[str, None]): Target membrane identifier for object movement.
        idx (Union[str, None]): Identifier for priority operations.
        mem_idx (Union[str, None]): Index identifier for membrane-specific operations.
    """

    def __init__(self,
                 left: ObjectsMultiset,
                 right: Dict[str, ObjectsMultiset],
                 prob: float = 1.0,
                 prior: Union[List[str], None] = None,
                 move: str = MoveCode.HERE,
                 destination: Union[str, None] = None,
                 idx: Union[str, None] = None,
                 mem_idx: Union[str, None] = None):
        """Initialize a new rule.
        
        Args:
            left (ObjectsMultiset): Multiset of objects consumed by the rule.
            right (ObjectsMultiset): Multiset of objects produced by the rule.
            prob (float, optional): Probability of rule application (0.0 to 1.0). 
                Defaults to 1.0.
            prior (float, optional): Priority level for rule selection. Higher 
                values indicate higher priority. Defaults to 1.0.
            move (str, optional): Movement code from MoveCode enum defining object 
                destination. Defaults to MoveCode.HERE.
            idx (Union[str, None], optional): Index identifier for membrane-specific 
                operations. Defaults to None.
        """
        self._left = left
        self._right = right
        self._prob = prob
        self._prior = prior
        self._move = move
        self._destination = destination
        self._idx = idx
        self._mem_idx = mem_idx

    def __repr__(self):
        """Return string representation of the rule.
        
        Returns:
            str: string showing all rule components including
                 left/right multisets, probability, priority, movement, 
                 destination, and index.
        """
        return f'RuleDMEM(idx={self._idx}, left={self._left.multiset}, right={self._right}, prob={self._prob}, prior={self._prior}, move={self._move}, destination={self._destination}, mem_idx={self._mem_idx})'
