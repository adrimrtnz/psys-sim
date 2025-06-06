from typing import Dict, List, Tuple

from src.classes.rule import Rule
from src.classes.membrane import Membrane

class PSystem:
    def __init__(self, alpha: Tuple, membranes: Dict[str, Membrane], rules: List[Rule], out=None):
        self._alpha = alpha
        self._membranes = membranes
        self._rules = rules
        # Si out=None, la salida es la membrana root, si no... configurar

    def print_membranes(self):
        self._membranes.print_structure()

    def print_rules(self):
        for membrane, rules in self._rules.items():
            if len(rules) != 0:
                print(membrane)
                for rule in rules:
                    print(f' - {rule}')