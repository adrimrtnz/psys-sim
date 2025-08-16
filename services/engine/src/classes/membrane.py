import numpy as np

from typing import List, Union, Self
from src.classes.rule import Rule
from src.classes.objects_multiset import ObjectsMultiset
from src.enums.constants import MoveCode


class Membrane:
    """Represents a single membrane within a P-system structure.

    A Membrane acts as a computational compartment, containing a multiset of
    objects and a set of rules that can be applied to them. Membranes are
    organized in a hierarchical (tree-like) structure, where each membrane
    can have one parent and multiple children.

    This class encapsulates the state of a membrane (its objects and structural
    relationships) and provides methods to manipulate this state by adding or
    removing child membranes and applying evolution rules.

    Attributes:
        id (str): A unique identifier for the membrane.
        multiplicity (int): The number of identical membranes of this type.
        capacity (int): The maximum number of objects the membrane can hold.
        parent (Optional[Membrane]): A reference to the parent membrane.
            None if it is the skin membrane.
        children (List[Membrane]): A list of child membranes contained within this one.
        objects (ObjectsMultiset): The multiset of objects present in the membrane's region.
    """

    def __init__(self, idx: str, multiplicity : int, capacity: int, parent: 'Membrane' = None):
        """Initializes a Membrane instance.

        Args:
            idx (str): The unique identifier for the membrane.
            multiplicity (int): The number of identical membranes.
            capacity (int): The maximum object capacity for this membrane.
            parent (Optional[Self], optional): The parent membrane in the hierarchy.
                Defaults to None.
        """
        self._id = idx
        self._m = multiplicity
        self._cap = capacity
        self._parent = parent
        self._children = []
        self._objects = ObjectsMultiset()

        self._alive = True
        self._step = 0

    def __repr__(self):
        """Provides a developer-friendly string representation of the membrane."""
        return f'Membrane - (id={self.id}, mul={self.multiplicity}, capacity={self.capacity})'

    @property
    def id(self) -> str:
        """Gets the membrane's unique identifier."""
        return self._id
    
    @property
    def multiplicity(self) -> int:
        """Gets the membrane's multiplicity."""
        return self._m
    
    @property
    def capacity(self) -> int:
        """Gets the membrane's maximum object capacity."""
        return self._cap
    
    @property
    def parent(self) -> Union[Self, None]:
        """Gets the parent of this membrane."""
        return self._parent
    
    @parent.setter
    def parent(self, value: 'Membrane'):
        """Sets or updates the parent membrane.

        This setter assigns a new parent to the membrane, ensuring type safety
        by validating that the assigned value is an instance of the Membrane class.

        Args:
            value (Membrane): The new parent membrane instance.

        Raises:
            ValueError: If the provided `value` is not an instance of the
                Membrane class.
        """
        if not isinstance(value, self.__class__):
            raise ValueError(f'Parent Membrane should be a instance of {self.__class__.__name__}')
        self._parent = value

    @property
    def children(self) -> List[Self]:
        """Gets the list of child membranes."""
        return self._children
    
    @property
    def objects(self):
        """Get the objects multiset of the membrane.
    
        Returns:
            ObjectsMultiset: The multiset containing membrane objects.
        """
        return self._objects
    
    @objects.setter
    def objects(self, new_value) -> ObjectsMultiset:
        """Set the objects multiset of the membrane.
    
        Args:
            new_value (ObjectsMultiset): The new objects multiset.
            
        Raises:
            TypeError: If new_value is not an ObjectsMultiset instance.
            ValueError: If new_value is None.
        """
        if new_value is None:
            raise ValueError('The membrane objects attribute cannot be None')
        if not isinstance(new_value, ObjectsMultiset):
            raise TypeError(f'Expected ObjectsMultiset, got {type(new_value).__name__}')
        self._objects = new_value
    
    def add_children(self, value: List[Self] | Self):
        """
        Function to add children to the Membrane

        Args:
            value: Membrane or list of Membranes
        """
        if type(value) is list:
            if all(isinstance(v, Membrane) for v in value):
                self._children.extend(value)
            else:
                raise ValueError('All the children to add should be an instance of Membrane')
        elif isinstance(value, Membrane):
            self._children.append(value)
    
    def add_child(self, child: Self):
        """Adds a single child membrane.

        Args:
            child (Self): The membrane to add as a child.

        Returns:
            bool: True upon successful addition.
        """
        self._children.append(child)
        return True

    def remove_child(self, child_idx) -> Self:
        """Removes and returns a child membrane by its index.

        Args:
            child_idx (int): The index of the child to remove.

        Returns:
            Self: The removed child membrane.
        """
        child = self._children.pop(child_idx)
        return child
    
    def apply_here_rule(self, rule: Rule, multiplicity : int):
        """Applies a rule where products remain in the same membrane.

        Consumes reactants from and adds products to this membrane's multiset.

        Args:
            rule (Rule): The rule to apply.
            multiplicity (int): The number of times the rule is applied.
        """
        for obj, m in rule.left.items():
            self.objects.sub_object(obj=obj, multiplicity=m * multiplicity)
        for obj, m in rule.right.items():
            self.objects.add_object(obj=obj, multiplicity=m * multiplicity)

    def apply_out_rule(self, rule: Rule, multiplicity : int):
        """Applies a rule where products are sent to the parent membrane.

        Consumes reactants from this membrane and adds products to the parent
        membrane's multiset. Does nothing with products if there is no parent.

        Args:
            rule (Rule): The rule to apply.
            multiplicity (int): The number of times the rule is applied.
        """
        for obj, m in rule.left.items():
            self.objects.sub_object(obj=obj, multiplicity=m * multiplicity)
        if self.parent is not None:
            for obj, m in rule.right.items():
                self.parent.objects.add_object(obj=obj, multiplicity=m * multiplicity)

    def apply_in_rule(self, rule: Rule, destination: 'Membrane', multiplicity : int):
        """Applies a rule where products are sent to a specific child membrane.

        Consumes reactants from this membrane and adds products to the specified
        destination child membrane's multiset.

        Args:
            rule (Rule): The rule to apply.
            destination (Self): The target child membrane for the products.
            multiplicity (int): The number of times the rule is applied.
        """
        for obj, m in rule.left.items():
            self.objects.sub_object(obj=obj, multiplicity=m * multiplicity)
        for obj, m in rule.right.items():
            destination.objects.add_object(obj=obj, multiplicity=m * multiplicity)

    def apply_move_mem_rule(self, rule: Rule, destination: 'Membrane', child_idx: int):
        """Applies a rule that moves a child membrane to another destination.

        The specified child is removed from this membrane's children, its
        internal state is evolved according to the rule, and it is then added
        to the destination membrane's children.

        Args:
            rule (Rule): The rule governing the state change of the moved child.
            destination (Self): The membrane to which the child will be moved.
            child_idx (int): The index of the child membrane to move.
        """
        child = self.remove_child(child_idx)
        child.apply_here_rule(rule, multiplicity=1)
        destination.add_child(child)
        child.parent = destination

    def apply_dissolve_to_parent_rule(self, rule: Rule):
        """Applies a rule that dissolves this membrane into its parent.

        First, the rule evolves the membrane's internal state. Then, all
        objects from this membrane are merged into the parent's multiset.
        Finally, this membrane is removed from its parent's children list and
        is destroyed.

        Args:
            rule (Rule): The final rule to apply before dissolving.
        """
        self.apply_here_rule(rule=rule, multiplicity=1)
        self.parent.objects = self.parent.objects + self.objects
        self.parent.children.remove(self)
        del self

    def apply_dmem_rule(self, rule: Rule, multiplicity: int):
        """Applies a division/differentiation rule (DMEM).

        This rule type consumes reactants from the current membrane and can
        produce objects in the current membrane ('HERE') or in sibling
        membranes ('DMEM') based on a target ID and probability.

        Args:
            rule (Rule): The DMEM rule to apply.
            multiplicity (int): The number of times the rule is applied.

        Raises:
            ValueError: If the rule contains an unhandled move code.
        """
        # parent -> building where self is
        parent = self.parent
        for obj, m in rule.left.items():
            self.objects.sub_object(obj=obj, multiplicity=m * multiplicity)
        
        # for each move there is a list of tuples (object, multiplicity, destination)
        for move in rule.right.keys():
            match move:
                case MoveCode.HERE.name:
                    for obj, m, _ in rule.right[move]:
                        self.objects.add_object(obj=obj, multiplicity=m * multiplicity)
                case MoveCode.DMEM.name:
                    for obj, m, idx in rule.right[move]:
                        # targets = aquellas membranas en la misma zona (parent) que no son self y coindicen con el destino
                        targets = [child for child in parent.children if child is not self and child.id == idx]
                        # aplicar la probabilidad de la regla por cada target posible
                        for target in targets:
                            if np.random.random() < rule.probability:
                                target.objects.add_object(obj=obj, multiplicity=m * multiplicity)
                case _:
                    raise ValueError(f'Case not handled for move="{move}" in rule with DMEM movement')

    def print_structure(self, level=0):
        """Prints the membrane structure recursively to the console.

        Args:
            level (int, optional): The current depth in the hierarchy for indentation.
                Defaults to 0.
        """
        print(f'{"   " * level}{str(self)}')
        for key, value in self.objects.items():
            print(f'{"   " * level}  BO - (v={key}, mul={value})')

        for child in self.children:
            child.print_structure(level + 1)

    def generate_html(self, level=0):
        html_output = f'<div class="rectangulo level-{level}">\n'
        html_output += f'  <div class="contenido">\n'
        html_output += f'    <h2>{str(self)}</h2>\n'
        html_output += f'<p>{str(self.objects)}'
        html_output += f'  </div>\n'

        for child in self.children:
            html_output += child.generate_html(level + 1)
        html_output += '</div>\n'
        return html_output

    def plot_structure(self, step: int):
        css_styles = """
        .rectangulo {
            border: 2px solid black; /* Borde del rectángulo */
            border-radius: 10px;     /* Esquinas redondeadas */
            padding: 10px;           /* Espacio interior */
            margin: 10px;            /* Espacio exterior */
            background-color: #f9f9f9;
        }
        .contenido h2 { margin-top: 0; color: #005a9c; }
        .contenido p { color: #c93756; font-family: monospace; }
        """
        body_content = self.generate_html()
        html_final = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>PSystem Step {step}</title>
            <style>{css_styles}</style>
        </head>
        <body>
        {body_content}
        </body>
        </html>
            """
        path = f'../../plots/{step:04}.html'
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(html_final)
