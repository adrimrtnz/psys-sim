from typing import Dict, Union
from src.enums.constants import MoveCode
from src.classes.objects_multiset import ObjectsMultiset

class Rule:
    def __init__(self, left: ObjectsMultiset, right: ObjectsMultiset, prob: float = 1.0, prior: float = 1.0, move: str = MoveCode.HERE, destination: Union[str, None] = None, idx: Union[str, None] = None):
        self._left = left
        self._right = right
        self._prob = prob
        self._prior = prior
        self._move = move
        self._destination = destination
        self._idx = idx

    def __repr__(self):
        return f'Rule(left={self._left.multiset}, right={self._right.multiset}, prob={self._prob}, prior={self._prior}, move={self._move}, destination={self._destination}, idx={self._idx})'


    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right
    
    @property
    def probability(self):
        return self._prob
    
    @property
    def priority(self):
        return self._prior
    
    @property
    def move(self):
        return self._move
    
    @property
    def destination(self):
        return self._destination
    
    @property
    def idx(self):
        return self._idx