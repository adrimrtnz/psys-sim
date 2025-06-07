from typing import Dict, List, Tuple

from src.classes.rule import Rule
from src.classes.membrane import Membrane
from src.enums.constants import InferenceType

class PSystem:
    def __init__(self, alpha: Tuple, membranes: Dict[str, Membrane], rules: List[Rule], out: str=None, inference: str='sequential'):
        self._alpha = alpha
        self._membranes = membranes
        self._rules = rules
        self._out = out
        self._inference = inference

    def print_membranes(self):
        # root = next(iter(self._membranes))
        # self._membranes[root].print_structure()
        self._membranes.print_structure()

    def print_rules(self):
        for membrane, rules in self._rules.items():
            if len(rules) != 0:
                print(membrane)
                for rule in rules:
                    print(f' - {rule}')

    def applicable_rules(self, membrane: Membrane):
        membrane_rules = self._rules[membrane.id]
        app_rules = []
        for rule in membrane_rules:
            left = rule.left
            for obj, m in left.items():
                if membrane.objects.count(obj) >= m:
                    app_rules.append(rule)
        return app_rules

    def applicable_rules_iter(self, membrane: Membrane):
        # print('Parent', membrane.id, "Children", len(membrane.children.keys()))
        rules = self.applicable_rules(membrane)
        print(membrane.id, rules)

        for child in membrane.children:
            self.applicable_rules_iter(child)

    def run(self):
        match self._inference:
            case InferenceType.SEQUENTIAL:
                self.__sequential()
            case _:
                raise NotImplementedError(f'Inference type "{self._inference}" not Implemented')

    def __sequential(self):
        print("Running sequential")
        self.applicable_rules_iter(self._membranes)