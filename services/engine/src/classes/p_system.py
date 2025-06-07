from typing import Dict, List, Tuple

from src.classes.rule import Rule
from src.classes.membrane import Membrane

class PSystem:
    def __init__(self, alpha: Tuple, membranes: Dict[str, Membrane], rules: List[Rule], out: str=None, inference: str='sequential'):
        self._alpha = alpha
        self._membranes = membranes
        self._rules = rules
        self._out = out
        self._inference = inference

    def print_membranes(self):
        root = next(iter(self._membranes))
        self._membranes[root].print_structure()

    def print_rules(self):
        for membrane, rules in self._rules.items():
            if len(rules) != 0:
                print(membrane)
                for rule in rules:
                    print(f' - {rule}')