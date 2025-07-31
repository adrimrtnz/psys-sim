import random
import numpy as np

from typing import Dict, List, Tuple, Union

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

    def seed(self, seed: Union[int, None]= None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed=seed)

    def __add_rule_to_apply(self, membrane:Membrane, rule_data: Tuple, multiplicity : int = 1):
        """Add a rule to the list of rules to be applied.
        
        Args:
            membrane (Membrane): The membrane where the rule will be applied.
            rule_data (Tuple): Data of the rule to be applied.
            multiplicity (int): How many times the rules will be applied.
        """
        self._rules_to_apply.append((membrane, rule_data, multiplicity))

    def __generate_maximal_group(self, membrane: Membrane, rules: List[Rule]):
        """Generates a single, non-deterministically chosen, maximal multiset of rules.

        This function implements an efficient, iterative ("greedy") algorithm to
        determine one valid multiset of rules to be applied in a single computation
        step, following the "maximally parallel" derivation mode. Instead of
        calculating all possible maximal sets (which is computationally expensive),
        it randomly selects rules one by one until no more rules can be applied to
        the remaining objects.

        The process is non-deterministic due to the random selection of rules at
        each iteration and the probabilistic application of each rule. The final
        multiset of rules is guaranteed to be "maximal" because the loop only
        terminates when the set cannot be extended further.

        The function categorizes the selected rules into two groups: those that
        affect objects ('obj') and those that affect the membrane itself ('mem'),
        such as dissolution rules.

        Pseudo-código del algoritmo:
        1.  Inicializar un 'grupo' de reglas vacío para almacenar el resultado.
        2.  Crear una copia de los objetos de la membrana para poder modificarlos.
        3.  Iniciar un bucle que se ejecuta mientras la lista de reglas a
            considerar no esté vacía.
        4.  Dentro del bucle:
            a.  Elegir una regla al azar de la lista de reglas disponibles.
            b.  Comprobar si la regla es aplicable con los objetos restantes.
            c.  Si NO es aplicable:
                i.  Eliminar la regla de la lista de reglas a considerar.
                ii. Continuar con la siguiente iteración del bucle.
            d.  Si ES aplicable:
                i.  Evaluar la probabilidad de la regla. Si la comprobación
                    probabilística falla, no se aplica la regla, pero el bucle
                    continúa para dar oportunidad a otras reglas.
                ii. Si la regla se aplica, añadirla al 'grupo' correspondiente
                    ('obj' o 'mem'), incrementando su contador.
                iii. Restar los objetos consumidos por la regla de la copia de
                    objetos de la membrana.
        5.  El bucle termina cuando la lista de reglas a considerar se vacía, lo que
            implica que no se pueden aplicar más reglas a los objetos restantes.
        6.  Devolver el 'grupo' de reglas final.

        Args:
            membrane (Membrane): El objeto de la membrana que contiene el
                multiconjunto actual de objetos sobre los que operar.
            rules (List): Una lista de todas las reglas inicialmente aplicables
                en esta membrana. Esta lista se modifica durante la ejecución de
                la función. Cuando una regla ya no es aplicable, se elimina.

        Returns:
            Dict: Un diccionario que contiene el multiconjunto de reglas
                seleccionado, categorizado por su tipo de efecto. La estructura es:
                {
                    'obj': {rule_idx: {'count': N, 'data': rule_data},...},
                    'mem': {rule_idx: {'count': M, 'data': rule_data},...}
                }
        """

        group = { 'obj': dict(), 'mem': dict() }
        if len(rules) > 0:
            original_objects = membrane.objects.copy()

            def select_rule():
                nonlocal original_objects
                if len(rules) == 0:
                    return False
                
                index = random.choice(range(len(rules)))
                rule_data = rules[index]
                rule = rule_data[-1]

                # Determine if the rule remains applicable
                count = original_objects.count_subsets(rule.left)

                if count > 0:
                    prob = rule.probability
                    if prob != 1.0:
                        probs = np.array([prob, 1-prob])
                        indexes = [1, -1]
                        rule_idx = np.random.choice(indexes, p=probs)
                        if rule_idx == -1:
                            return True
                    branch = 'obj' if rule.move not in (MoveCode.DISS_KEEP.name, MoveCode.DISS.name) else 'mem'
                    is_applied = group[branch].get(rule.idx, False)
                    if is_applied:
                        group[branch][rule.idx]['count'] = group[branch][rule.idx]['count'] + 1
                    else:
                        group[branch][rule.idx] = dict()
                        group[branch][rule.idx]['count'] = 1
                        group[branch][rule.idx]['data'] = rule_data
                    original_objects = original_objects - rule.left                            
                else:
                    # Remove the rule if not applicable
                    del rules[index]
                return True
            
            while select_rule():
                # Avoiding recursion to prevent stack overflow due to excessive calls
                pass
        return group
    
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

        app_obj_rules = []              # Rules with defined priorities
        app_mem_rules = []              # Rules that move an entire membrane
        app_rules_idxs = []             # List of IDs of the applicable rules

        for rule in membrane_obj_rules:
            left = rule.left
            if all(membrane.objects.count(obj) >= m for obj, m in left.items()):
                if rule.priority is not None:
                    if not (set(app_rules_idxs) & set(rule.priority)):
                        app_obj_rules.append((membrane.id, 0, 0, rule))
                        app_rules_idxs.append(rule.idx)
                else:
                    app_obj_rules.append((membrane.id, 0, 0, rule))
                    app_rules_idxs.append(rule.idx)

        for i, child in enumerate(membrane.children):
            for rule in membrane_mem_rules:
                idx = rule.idx
                if child.id == idx and all(child.objects.count(obj) >= m for obj, m in rule.left.items()):
                    app_mem_rules.append((membrane.id, child.id, i, rule))
        return app_obj_rules + list(reversed(app_mem_rules))
    
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
        rules = self.applicable_rules(membrane)

        if len(rules) > 0:
            probs = np.array([rule.probability for _,_,_,rule in rules])
            total_prob = probs.sum()
            indexes = list(range(len(rules)))

            if total_prob > 1.0:
                # Normalize if prob is greater than 1.0
                probs /= total_prob
            elif total_prob < 1.0:
                probs = np.append(probs, 1 - total_prob)
                indexes += [-1]
            rule_idx = np.random.choice(indexes, p=probs)
            if rule_idx != -1:
                to_apply = rules[rule_idx]
                self.__add_rule_to_apply(membrane, to_apply)

        for child in membrane.children:
            self.min_par_step(child, trace_file=trace_file)

    def __sample_binomial_successes(self, num_trials: int, probability: float):
        """Draws a single sample from a binomial distribution.

        This utility function determines the number of successful outcomes from
        a series of independent Bernoulli trials using NumPy's vectorized operations.
        This is statistically equivalent to drawing one sample from a binomial
        distribution B(n, p), where n is num_trials and p is the probability.

        It is used to calculate how many potential rule applications actually
        occur, given a specific probability for each.

        Args:
            num_trials (int): The number of trials to perform, corresponding
                to the number of potential rule applications.
            probability (float): The probability of success (i.e., the rule is
                applied) for each trial. Must be between 0.0 and 1.0.

        Returns:
            int: The total number of successful trials, an integer between 0
                and num_trials.
        """
        if num_trials == 0:
            return 0
        return int((np.random.random(num_trials) < probability).sum())

    def max_par_step(self, membrane: Membrane, trace_file=None):
        """Execute one step of maximally parallel inference.
        
        Finds applicable rules for a membrane, computes a random
        non-extendable set of rules, and applies it. Recursively
        processes all child membranes.
        
        Args:
            membrane (Membrane): The membrane to process.
            trace_file (file, optional): File object to write trace information.
                Defaults to None.
        """
        rules = self.applicable_rules(membrane)
        group = self.__generate_maximal_group(membrane=membrane, rules=rules)

        for type in ['obj', 'mem']:
            for _, item in group[type].items():
                rule_data = item['data']
                count = item['count']
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
                print(f'{"="*15} STEP {counter} {"="*15}')
                self.print_membranes()
                # self._membranes.plot_structure(counter)
        finally:
            out.close()