from typing import Dict, Union
from src.enums.constants import MoveCodes

class Rule:
    def __init__(self, left: Dict, right: Dict, prob = 1, prior = 1, move: str = MoveCodes.HERE, destination: Union[str, None] = None):
        self._left = left
        self._right = right
        self._prob = prob
        self._prior = prior
        self._move = move
        self._destination = destination

    def __repr__(self):
        return f'Rule(right={self._left}, left={self._right}, prob={self._prob}, prior={self._prior}, move={self._move}, destination={self._destination})'
