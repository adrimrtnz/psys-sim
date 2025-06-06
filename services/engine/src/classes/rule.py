from typing import Dict
from src.enums.constants import MoveCodes

class Rule:
    def __init__(self, left: Dict, right: Dict, prob = 1, prior = 1, type: str = MoveCodes.HERE):
        self._left = left
        self._right = right
        self._prob = prob
        self._prior = prior
        self._type = type

    def __repr__(self):
        return f'Rule(right={self._left}, left={self._right}, prob={self._prob}, prior={self._prior}, type={self._type})'
