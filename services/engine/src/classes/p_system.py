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

    def __add_rule_to_apply(self, membrane:Membrane, rule_data: Tuple, multiplicity : int = 1):
        """Add a rule to the list of rules to be applied.
        
        Args:
            membrane (Membrane): The membrane where the rule will be applied.
            rule_data (Tuple): Data of the rule to be applied.
            multiplicity (int): How many times the rules will be applied.
        """
        self._rules_to_apply.append((membrane, rule_data, multiplicity))

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
        app_obj_priority_rules = []
        app_diss_rules = []
        app_mem_rules = []
        max_priority = -1

        for rule in membrane_obj_rules:
            left = rule.left
            if all(membrane.objects.count(obj) >= m for obj, m in left.items()):
                if rule.priority is not None:
                    if rule.priority > max_priority:
                        max_priority = rule.priority
                        print(f'Max priority: {max_priority} en membrana {membrane.id}')
                        # If we find a more dominant rule over the already seen ones, clear the list
                        app_obj_priority_rules.clear()
                    if rule.priority < max_priority:
                        continue
                    if rule.move in [MoveCode.DISS_KEEP.name]:
                        app_diss_rules.append((membrane.id, 0, 0, rule))
                    else:
                        app_obj_priority_rules.append((membrane.id, 0, 0, rule))
                else:
                    if rule.move in [MoveCode.DISS_KEEP.name]:
                        app_diss_rules.append((membrane.id, 0, 0, rule))
                    else:
                        app_obj_rules.append((membrane.id, 0, 0, rule))

        for i, child in enumerate(membrane.children):
            for rule in membrane_mem_rules:
                idx = rule.idx
                if child.id == idx and all(child.objects.count(obj) >= m for obj, m in rule.left.items()):
                    app_mem_rules.append((membrane.id, child.id, i, rule))
        app_obj_rules = app_obj_rules + app_obj_priority_rules + app_diss_rules
        return app_obj_rules, list(reversed(app_mem_rules))
    
    def apply_rule(self, membrane: Membrane, data, multiplicity: int = 1):
        """Apply a specific rule to a membrane.
        
        Executes a rule based on its movement code, handling different types
        of membrane operations such as OUT, HERE, IN, and MEMwOB.
        
        Args:
            membrane (Membrane): The membrane where the rule is applied.
            data: Tuple containing (mem_id, child_id, child_index, rule).
            multiplicity (int): How many times the rules will be applied.
        Returns:
            str: Trace message describing the rule application.
        """
        mem_id, child_id, child_index, rule = data
        move = rule.move
        match move:
            case MoveCode.OUT.name:
                trace = f' - Applying OUT {membrane.id:>8} -> {multiplicity} x {rule}'
                membrane.apply_out_rule(rule=rule, multiplicity=multiplicity)
            case MoveCode.HERE.name:
                trace = f' - Applying HERE {membrane.id:>7} -> {multiplicity} x {rule}'
                membrane.apply_here_rule(rule=rule, multiplicity=multiplicity)
            case MoveCode.IN.name:
                dest_idx = rule.destination
                # For simplicity in this state of the development. In the given scenario IN rules are applied from parent to children
                dest = next((child for child in membrane.children if child.id == dest_idx))
                trace = f' - Applying IN {membrane.id:>9} -> {multiplicity} x {rule}'
                membrane.apply_in_rule(rule=rule, destination=dest, multiplicity=multiplicity)
            case MoveCode.MEMwOB.name:
                dest_idx = rule.destination
                dest = next((child for child in self._membranes.children if child.id == dest_idx))
                trace = f' - Applying MEMwOB {membrane.id:>5} -> {rule}, Child Nº {child_index} from {mem_id} to {dest.id}'
                membrane.apply_move_mem_rule(rule=rule, destination=dest, child_idx=child_index)
            case MoveCode.DISS_KEEP.name:
                trace = f' - Applying DISS_KEEP {membrane.id:>2} -> {rule}'
                membrane.apply_dissolve_to_parent_rule(rule=rule)
            case _:
                trace = f' - NOT Applied {membrane.id:>5} -> {rule}'
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
        for membrane, data, multiplicity in self._rules_to_apply:
            trace = self.apply_rule(membrane=membrane, data=data, multiplicity=multiplicity)
            print(trace, file=trace_file)
        self._rules_to_apply.clear()
        return n_rules > 0

    def min_par_step(self, membrane: Membrane, trace_file=None):
        """Execute one step of minimally parallel inference.
        
        Finds applicable rules for a membrane and probabilistically selects
        one for application. Recursively processes all child membranes.
        
        Args:
            membrane (Membrane): The membrane to process.
            trace_file (file, optional): File object to write trace information.
                Defaults to None.
        """
        obj_rules_data, mem_rule_data = self.applicable_rules(membrane)
        all_rules_data = obj_rules_data + mem_rule_data

        if len(all_rules_data) > 0:
            probs = np.array([rule.probability for _,_,_,rule in all_rules_data])
            total_prob = probs.sum()
            indexes = list(range(len(all_rules_data)))

            if total_prob > 1.0:
                # Normalize if prob is greater than 1.0
                probs /= total_prob
            elif total_prob < 1.0:
                probs = np.append(probs, 1 - total_prob)
                indexes += [-1]
            rule_idx = np.random.choice(indexes, p=probs)
            if rule_idx != -1:
                to_apply = all_rules_data[rule_idx]
                self.__add_rule_to_apply(membrane, to_apply)

        for child in membrane.children:
            self.min_par_step(child, trace_file=trace_file)

    def max_par_step(self, membrane: Membrane, trace_file=None):
        """Execute one step of maximally parallel inference.
        
        Finds applicable rules for a membrane, computes the set of
        non-extendable sets of rules, and applies one of the sets
        stochastically. Recursively processes all child membranes.
        
        Args:
            membrane (Membrane): The membrane to process.
            trace_file (file, optional): File object to write trace information.
                Defaults to None.
        """
        obj_rules_data, mem_rule_data = self.applicable_rules(membrane)
        all_rules_data = obj_rules_data + mem_rule_data
        groups_of_rules = list()

        if len(all_rules_data) > 0:
            original_objects = membrane.objects.copy()
            for rule_data in all_rules_data:
                rule = rule_data[-1]
                prob = rule.probability
                probs = np.array([prob, 1-prob])
                indexes = [1, -1]
                rule_idx = np.random.choice(indexes, p=probs)
                if rule_idx != -1:
                    rule_left = rule.left
                    count = original_objects.count_subsets(rule_left)
                    original_objects.sub(rule_left)
                    self.__add_rule_to_apply(membrane=membrane, rule_data=rule_data, multiplicity=count)

        for child in membrane.children:
            self.max_par_step(child, trace_file=trace_file)

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
            case InferenceType.MAX_PARALLEL:
                self.__maxpar(max_steps=max_steps)
            case _:
                raise NotImplementedError(f'Inference type "{self._inference}" not Implemented')

    def __minpar(self, max_steps=None):
        """Execute minimally parallel inference mode.
        
        Runs the P-System using minimally parallel inference, where at each step
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

    def __maxpar(self, max_steps=None):
        """Execute maximally parallel inference mode.
        
        Runs the P-System using maximally parallel inference,
        where at each step, a non-extendable number of rules.
        
        Args:
            max_steps (int, optional): Maximum number of steps to execute.
                If None, runs until no more rules are applicable.
        """
        print("Running Max. Parallel")
        try:
            out = open('../../plots/run_trace.txt', 'w+', encoding='utf-8')
            has_applied = True
            counter = 0
            self._membranes.plot_structure(counter)
            while has_applied and (max_steps is None or counter < max_steps):
                counter += 1
                print(f'{"="*15} STEP {counter} {"="*15}', file=out)
                self.max_par_step(self._membranes, out)
                has_applied = self.apply_rules(out)
                # self._membranes.plot_structure(counter)
        finally:
            out.close()