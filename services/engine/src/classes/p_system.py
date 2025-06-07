import random

from typing import Dict, List, Tuple

from src.classes.rule import Rule
from src.classes.membrane import Membrane
from src.enums.constants import InferenceType, MoveCode

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
    
    def apply_rule(self, membrane: Membrane, rule: Rule):
        move = rule.move
        match move:
            case MoveCode.OUT.name:
                # TODO: Refactorizar esto
                for obj, m in rule.left.items():
                    membrane.objects.sub(obj=obj, multiplicity=m)
                for obj, m in rule.right.items():
                    membrane.parent.objects.add(obj=obj, multiplicity=m)

    def seq_step(self, membrane: Membrane):
        rules = self.applicable_rules(membrane)
        if len(rules) > 0:
            to_apply = random.choice(rules)
            self.apply_rule(membrane, to_apply)

        for child in membrane.children:
            self.seq_step(child)


    def run(self):
        match self._inference:
            case InferenceType.SEQUENTIAL:
                self.__sequential()
            case _:
                raise NotImplementedError(f'Inference type "{self._inference}" not Implemented')

    def __sequential(self):
        print("Running sequential")
        self.seq_step(self._membranes)