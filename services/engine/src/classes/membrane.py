from typing import List
from src.classes.rule import Rule
from src.classes.objects_multiset import ObjectsMultiset


class Membrane:
    def __init__(self, idx: str, multiplicity : int, capacity: int, parent: 'Membrane' = None):
        self._id = idx
        self._m = multiplicity
        self._cap = capacity
        self._parent = parent
        self._children = []
        self._objects = ObjectsMultiset()
        self._rules = None

        self._alive = True
        self._step = 0

    def __repr__(self):
        return f'Membrane - (id={self.id}, mul={self.multiplicity}, capacity={self.capacity})'

    @property
    def id(self):
        return self._id
    
    @property
    def multiplicity(self):
        return self._m
    
    @property
    def capacity(self):
        return self._cap
    
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return self._children
    
    @property
    def objects(self):
        """Get the objects multiset of the membrane.
    
        Returns:
            ObjectsMultiset: The multiset containing membrane objects.
        """
        return self._objects
    
    @objects.setter
    def objects(self, new_value):
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
    
    @property
    def rules(self):
        return self._rules
    
    @rules.setter
    def rules(self, new_rules):
        self._rules = new_rules
    
    def add_children(self, value: List['Membrane'] | 'Membrane'):
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
    
    def add_child(self, child: 'Membrane'):
        self._children.append(child)
        return True

    def remove_child(self, child_idx):
        child = self._children.pop(child_idx)
        return child
    
    def apply_here_rule(self, rule: Rule, multiplicity : int):
        for obj, m in rule.left.items():
            self.objects.sub_object(obj=obj, multiplicity=m * multiplicity)
        for obj, m in rule.right.items():
            self.objects.add_object(obj=obj, multiplicity=m * multiplicity)

    def apply_out_rule(self, rule: Rule, multiplicity : int):
        for obj, m in rule.left.items():
            self.objects.sub_object(obj=obj, multiplicity=m * multiplicity)
        if self.parent is not None:
            for obj, m in rule.right.items():
                self.parent.objects.add_object(obj=obj, multiplicity=m * multiplicity)

    def apply_in_rule(self, rule: Rule, destination: 'Membrane', multiplicity : int):
        for obj, m in rule.left.items():
            self.objects.sub_object(obj=obj, multiplicity=m * multiplicity)
        for obj, m in rule.right.items():
            destination.objects.add_object(obj=obj, multiplicity=m * multiplicity)

    def apply_move_mem_rule(self, rule: Rule, destination: 'Membrane', child_idx: int):
        child = self.remove_child(child_idx)
        child.apply_here_rule(rule)
        destination.add_child(child)
        child.parent = destination

    def apply_dissolve_to_parent_rule(self, rule: Rule):
        self.apply_here_rule(rule=rule, multiplicity=1)
        self.parent.objects = self.parent.objects + self.objects
        self.parent.children.remove(self)
        del self

    def print_structure(self, level=0):
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
