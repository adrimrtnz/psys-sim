import numpy as np

from typing import Dict, List, Tuple

from src.classes.rule import Rule
from src.classes.membrane import Membrane
from src.enums.constants import InferenceType, MoveCode, SceneObject

"""
P-System implementation module for membrane computing.

This module provides the main PSystem class that orchestrates the execution
of membrane computing systems, including rule application, inference modes,
and system evolution.
"""

class PSystem:
    """P-System implementation for membrane computing simulations.
    
    A P-System represents a membrane computing model that consists of membranes
    containing objects and rules. The system can evolve through the application
    of rules according to different inference modes.
    
    Attributes:
        alpha (Tuple): Alphabet of objects used in the system.
        membranes (Membrane): Root membrane containing the membrane structure.
        rules (Dict[str, Rule]): Dictionary mapping membrane IDs to their rules.
        out (str): Output membrane identifier (optional).
        inference (str): Inference mode for rule application.
        rules_to_apply (List): List of rules pending application.
    """

    def __init__(self, alpha: Tuple, membranes: Membrane, rules: Dict[str, Rule], out: str=None, inference: str=InferenceType.MIN_PARALLEL):
        """Initialize a P-System.
        
        Args:
            alpha (Tuple): Alphabet of objects that can appear in the system.
            membranes (Membrane): Root membrane of the system structure.
            rules (Dict[str, Rule]): Dictionary mapping membrane identifiers to rules.
            out (str, optional): Identifier of the output membrane. Defaults to None -> out = root membrane.
            inference (str, optional): Inference mode to use. Defaults to MIN_PARALLEL.
        """
        self._alpha = alpha
        self._membranes = membranes
        self._rules = rules
        self._out = out
        self._inference = inference
        self._rules_to_apply = []

    def __add_rule_to_apply(self, membrane:Membrane, rule: Rule):
        """Add a rule to the list of rules to be applied.
        
        Args:
            membrane (Membrane): The membrane where the rule will be applied.
            rule (Rule): The rule to be applied.
        """
        self._rules_to_apply.append((membrane, rule))

    def print_membranes(self):
        """Print the membrane structure of the system.
        
        Displays the hierarchical structure of membranes in the P-System.
        """
        # root = next(iter(self._membranes))
        # self._membranes[root].print_structure()
        self._membranes.print_structure()

    def print_rules(self):
        """Print all rules in the system organized by membrane.
        
        Displays all rules grouped by their corresponding membranes,
        showing only membranes that have rules defined.
        """
        for membrane, rules in self._rules.items():
            if len(rules) != 0:
                print(membrane)
                for rule in rules:
                    print(f' - {rule}')

    def applicable_rules(self, membrane: Membrane):
        """Find all applicable rules for a given membrane.
        
        Determines which object and membrane rules can be applied in the current
        state of the membrane, considering rule priorities and object availability.
        
        Args:
            membrane (Membrane): The membrane to check for applicable rules.
            
        Returns:
            Tuple[List, List]: A tuple containing:
                - List of applicable object rules
                - List of applicable membrane rules (in reversed order)
        """
        membrane_obj_rules = self._rules.get((membrane.id, SceneObject.OBJECT_RULE), [])
        membrane_mem_rules = self._rules.get((membrane.id, SceneObject.MEMBRANE_RULE), [])
        app_obj_rules = []
        app_mem_rules = []
        max_priority = -1

        for rule in membrane_obj_rules:
            left = rule.left
            if all(membrane.objects.count(obj) >= m for obj, m in left.items()):
                if rule.priority > max_priority:
                    max_priority = rule.priority
                    # If we find a more dominant rule over the already seen ones, clear the list
                    app_obj_rules.clear()
                if rule.priority < max_priority:
                    continue
                app_obj_rules.append((membrane.id, 0, 0, rule))

        for i, child in enumerate(membrane.children):
            for rule in membrane_mem_rules:
                idx = rule.idx
                if child.id == idx and all(child.objects.count(obj) >= m for obj, m in rule.left.items()):
                    app_mem_rules.append((membrane.id, child.id, i, rule))
        return app_obj_rules, list(reversed(app_mem_rules))
    
    def apply_rule(self, membrane: Membrane, data):
        """Apply a specific rule to a membrane.
        
        Executes a rule based on its movement code, handling different types
        of membrane operations such as OUT, HERE, IN, and MEMwOB.
        
        Args:
            membrane (Membrane): The membrane where the rule is applied.
            data: Tuple containing (mem_id, child_id, child_index, rule).
            
        Returns:
            str: Trace message describing the rule application.
        """
        mem_id, child_id, child_index, rule = data
        move = rule.move
        match move:
            case MoveCode.OUT.name:
                trace = f' - Applicando OUT {membrane.id:>8} -> {rule}'
                membrane.apply_out_rule(rule=rule)
            case MoveCode.HERE.name:
                trace = f' - Applicando HERE {membrane.id:>7} -> {rule}'
                membrane.apply_here_rule(rule=rule)
            case MoveCode.IN.name:
                dest_idx = rule.destination
                # For simplicity in this state of the development. In the given scenario IN rules are applied from parent to children
                dest = next((child for child in membrane.children if child.id == dest_idx))
                trace = f' - Applicando IN {membrane.id:>9} -> {rule}'
                membrane.apply_in_rule(rule=rule, destination=dest)
            case MoveCode.MEMwOB.name:
                dest_idx = rule.destination
                dest = next((child for child in self._membranes.children if child.id == dest_idx))
                trace = f' - Applicando MEMwOB {membrane.id:>5} -> {rule}, Child Nº {child_index} from {mem_id} to {dest.id}'
                membrane.apply_move_mem_rule(rule=rule, destination=dest, child_idx=child_index)
            case _:
                trace = f' - NO Applicada {membrane.id:>5} -> {rule}'
        return trace

    def apply_rules(self, trace_file = None):
        """Apply all pending rules in the system.
        
        Executes all rules that have been scheduled for application and
        clears the pending rules list.
        
        Args:
            trace_file (file, optional): File object to write trace information.
                Defaults to None.
                
        Returns:
            bool: True if at least one rule was applied, False otherwise.
        """
        n_rules = len(self._rules_to_apply)
        for m, data in self._rules_to_apply:
            trace = self.apply_rule(m, data)
            print(trace, file=trace_file)
        self._rules_to_apply.clear()
        return n_rules > 0

    def min_par_step(self, membrane: Membrane, trace_file=None):
        """Execute one step of minimal parallel inference.
        
        Finds applicable rules for a membrane and probabilistically selects
        one for application. Recursively processes all child membranes.
        
        Args:
            membrane (Membrane): The membrane to process.
            trace_file (file, optional): File object to write trace information.
                Defaults to None.
        """
        obj_rules, mem_rule = self.applicable_rules(membrane)
        all_rules = obj_rules + mem_rule

        if len(all_rules) > 0:
            probs = np.array([rule.probability for _,_,_,rule in all_rules])
            total_prob = probs.sum()
            indexes = list(range(len(all_rules)))

            if total_prob > 1.0:
                # Normalize if prob is greater than 1.0
                probs /= total_prob
            elif total_prob < 1.0:
                probs = np.append(probs, 1 - total_prob)
                indexes += [-1]
            rule_idx = np.random.choice(indexes, p=probs)
            if rule_idx != -1:
                to_apply = all_rules[rule_idx]
                self.__add_rule_to_apply(membrane, to_apply)

        for child in membrane.children:
            self.min_par_step(child, trace_file=trace_file)

    def run(self, max_steps=None):
        """Run the P-System simulation.
        
        Executes the P-System according to the specified inference mode
        for a maximum number of steps or until no more rules can be applied.
        
        Args:
            max_steps (int, optional): Maximum number of steps to execute.
                If None, runs until no more rules are applicable.
                
        Raises:
            NotImplementedError: If the specified inference type is not implemented.
        """
        match self._inference:
            case InferenceType.MIN_PARALLEL:
                self.__minpar(max_steps=max_steps)
            case _:
                raise NotImplementedError(f'Inference type "{self._inference}" not Implemented')

    def __minpar(self, max_steps=None):
        """Execute minimal parallel inference mode.
        
        Runs the P-System using minimal parallel inference, where in each step
        at most one rule is applied per membrane, selected probabilistically.
        
        Args:
            max_steps (int, optional): Maximum number of steps to execute.
                If None, runs until no more rules are applicable.
        """
        print("Running Min. Parallel")
        try:
            out = open('../../plots/run_trace.txt', 'w+', encoding='utf-8')
            has_applied = True
            counter = 0
            self._membranes.plot_structure(counter)
            while has_applied and (max_steps is None or counter < max_steps):
                counter += 1
                print(f'{"="*15} STEP {counter} {"="*15}', file=out)
                self.min_par_step(self._membranes, out)
                has_applied = self.apply_rules(out)
                self._membranes.plot_structure(counter)
        finally:
            out.close()