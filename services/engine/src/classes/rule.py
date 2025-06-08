from typing import Dict, Union
from src.enums.constants import MoveCode

class Rule:
    def __init__(self, left: Dict, right: Dict, prob = 1, prior = 1, move: str = MoveCode.HERE, destination: Union[str, None] = None):
        self._left = left
        self._right = right
        self._prob = prob
        self._prior = prior
        self._move = move
        self._destination = destination

    def __repr__(self):
        return f'Rule(left={self._left}, right={self._right}, prob={self._prob}, prior={self._prior}, move={self._move}, destination={self._destination})'


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