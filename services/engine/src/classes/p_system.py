import random

from typing import Dict, List, Tuple

from src.classes.rule import Rule
from src.classes.membrane import Membrane
from src.enums.constants import InferenceType, MoveCode

class PSystem:
    def __init__(self, alpha: Tuple, membranes: Membrane, rules: List[Rule], out: str=None, inference: str='sequential'):
        self._alpha = alpha
        self._membranes = membranes
        self._rules = rules
        self._out = out
        self._inference = inference
        self._rules_to_apply = []

    def __add_rule_to_apply(self, membrane:Membrane, rule: Rule):
        self._rules_to_apply.append((membrane, rule))

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
            if all(membrane.objects.count(obj) >= m for obj, m in left.items()):
                app_rules.append(rule)
        return app_rules
    
    def apply_rule(self, membrane: Membrane, rule: Rule):
        move = rule.move
        match move:
            case MoveCode.OUT.name:
                print(f' - Applicando OUT {membrane.id:>8} -> {rule}')
                membrane.apply_out_rule(rule=rule)
            case MoveCode.HERE.name:
                print(f' - Applicando HERE {membrane.id:>7} -> {rule}')
                membrane.apply_here_rule(rule=rule)
            case MoveCode.IN.name:
                dest_idx = rule.destination
                # For simplicity in this state of the development. In the given scenario IN rules are applied from parent to children
                dest = next((child for child in membrane.children if child.id == dest_idx))
                print(f' - Applicando IN {membrane.id:>9} -> {rule}')
                membrane.apply_in_rule(rule=rule, destination=dest)
            case _:
                print(f' - NO Applicada {membrane.id:>10} -> {rule}')

    def apply_rules(self):
        n_rules = len(self._rules_to_apply)
        for m, r in self._rules_to_apply:
            self.apply_rule(m, r)
        self._rules_to_apply.clear()
        return n_rules > 0

    def seq_step(self, membrane: Membrane):
        rules = self.applicable_rules(membrane)

        if len(rules) > 0:
            to_apply = random.choice(rules) # TODO: Apply priority
            self.__add_rule_to_apply(membrane, to_apply)
        
        for child in membrane.children:
            self.seq_step(child)

    def run(self, max_steps=None):
        match self._inference:
            case InferenceType.SEQUENTIAL:
                self.__sequential(max_steps=max_steps)
            case _:
                raise NotImplementedError(f'Inference type "{self._inference}" not Implemented')

    def __sequential(self, max_steps=None):
        print("Running sequential")
        has_applied = True
        counter = 0
        while has_applied and (max_steps is None or counter < max_steps):
            print(f'{"="*15} STEP {counter + 1} {"="*15}')
            self.seq_step(self._membranes)
            has_applied = self.apply_rules()
            # self._membranes.print_structure()
            counter += 1