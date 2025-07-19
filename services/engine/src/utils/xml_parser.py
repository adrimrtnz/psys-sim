from collections import deque
from typing import Dict, List, Tuple
from xml.dom import minidom

from src.classes.rule import Rule
from src.classes.objects_multiset import ObjectsMultiset
from src.classes.membrane import Membrane
from src.classes.p_system import PSystem
from src.enums.constants import SceneObject

class XMLInputParser:
    def __init__(self, config):
        scene_doc = minidom.parse(f'../../scenes/{config.scene}.xml')
        
        self._config = config
        self._rules = minidom.parse(f'../../rules/{config.rules}.xml')
        self._scene_root = scene_doc.getElementsByTagName('config')[0]

    def iterate_scene_node(self, node, parent : None | Membrane = None ) -> Membrane:
        for child in node.childNodes:
            if child.nodeType == minidom.Node.ELEMENT_NODE:
                attr = self.__get_node_attributes(child)

                if child.nodeName == SceneObject.MEMBRANE:
                    m_id, m_mul, m_cap = attr
                    membrane = Membrane(idx=m_id, multiplicity=m_mul, capacity=m_cap)
                    if parent:
                        parent.add_children(membrane)
                        membrane.parent = parent
                    else:
                        parent = membrane
                    self.iterate_scene_node(child, membrane)
                elif child.nodeName == SceneObject.OBJECT:
                    bo_v, bo_mul = attr
                    parent.objects.add_object(bo_v, bo_mul)
        return parent
    
    def iterate_rules_node(self, node: minidom.Document) -> Tuple[List[str], Dict]:
        alphabet = []
        rules_mapping = dict()

        alphabet_node = node.getElementsByTagName('alphabet')[0].getElementsByTagName('v')
        membranes = node.getElementsByTagName('membranes')[0]

        for item in alphabet_node:
            alphabet.append(item.getAttribute('value'))
        alphabet = tuple(alphabet)

        for membrane in membranes.childNodes:
            if membrane.nodeName == SceneObject.MEMBRANE:
                idx = membrane.getAttribute('ID')
                obj_rules = membrane.getElementsByTagName(SceneObject.OBJECT_RULE)
                mem_rules = membrane.getElementsByTagName(SceneObject.MEMBRANE_RULE)
                
                membrane_obj_rules = []
                membrane_mem_rules = []
                for rule in obj_rules:
                    built_rule = self.__build_obj_rule(rule)
                    membrane_obj_rules.append(built_rule)

                for rule in mem_rules:
                    built_rule = self.__build_mem_rule(rule)
                    membrane_mem_rules.append(built_rule)
                rules_mapping[idx, SceneObject.OBJECT_RULE] = membrane_obj_rules
                rules_mapping[idx, SceneObject.MEMBRANE_RULE] = membrane_mem_rules
        return alphabet, rules_mapping

    def __build_obj_rule(self, rule_node) -> Rule:
        idx = rule_node.getAttribute('id')
        probability = float(rule_node.getAttribute('pb')) if rule_node.getAttribute('pb') else 1.0
        priority = self.__extract_rule_priority(rule_node=rule_node)
        left_objects, _, _ = self.__extract_rule_objects(rule_node.getElementsByTagName(SceneObject.RULE_LH))
        right_objects, move, dest = self.__extract_rule_objects(rule_node.getElementsByTagName(SceneObject.RULE_RH))
        rule = Rule(idx=idx,
                    left=left_objects,
                    right=right_objects,
                    prob=probability,
                    prior=priority,
                    move=move,
                    destination=dest)
        return rule
    
    def __build_mem_rule(self, rule_node) -> Rule:
        idx = rule_node.getAttribute('id')
        probability = float(rule_node.getAttribute('pb'))
        priority = self.__extract_rule_priority(rule_node=rule_node)
        left_objects, _, _, _ = self.__extract_rule_membrane_objects(rule_node.getElementsByTagName(SceneObject.RULE_LH))
        right_objects, move, dest, mem_idx = self.__extract_rule_membrane_objects(rule_node.getElementsByTagName(SceneObject.RULE_RH))
        rule = Rule(idx=idx,
                    left=left_objects,
                    right=right_objects,
                    prob=probability,
                    prior=priority,
                    move=move,
                    destination=dest,
                    mem_idx=mem_idx)
        return rule

    def __extract_rule_objects(self, nodes) -> Tuple[Dict, str | None]:
        out = ObjectsMultiset()
        if len(nodes) == 0:
            return out, None, None
        nodes = nodes[0]
        move = nodes.getAttribute('move') if nodes.nodeName == SceneObject.RULE_RH else None
        objects = nodes.getElementsByTagName(SceneObject.OBJECT)
        dest = nodes.getAttribute('destination') if nodes.hasAttribute('destination') else None
        for obj in objects:
            value = obj.getAttribute('v')
            mult = int(obj.getAttribute('m'))
            out.add_object(value, mult)
        return out, move, dest
    
    def __extract_rule_membrane_objects(self, nodes) -> Tuple[Dict, str | None]:
        if len(nodes) == 0:
            return dict(), None, None
        mem_idx = nodes[0].getElementsByTagName('MEMwOB')[0].getAttribute('id')
        return *self.__extract_rule_objects(nodes), mem_idx
    
    def __extract_rule_priority(self, rule_node):
        priority = rule_node.getAttribute('pr')
        if priority:
            return priority.split(',')
        return None

    def __flatten_membrane_tree(self, root: Membrane):
        """
        Flatten the membrane tree into a dictionary to O(1) access time.

        (WIP): Repensar esto, porque al tener membranas con mismo nombre (e.g. h1) colisiona
        """
        out = dict()
        membrane_queue = deque([root])        

        while membrane_queue:
            membrane = membrane_queue.popleft()
            out[membrane.id] = membrane
            membrane_queue.extend(membrane.children)
        return out

    @staticmethod
    def __get_node_attributes(node) -> List[str] | None:
        if node.nodeName == SceneObject.OBJECT:
            bo_v = node.getAttribute('v')
            bo_mul = int(node.getAttribute('m'))
            return  bo_v, bo_mul
        if node.nodeName == SceneObject.MEMBRANE:
            m_id  = node.getAttribute('id')
            m_mul = int(node.getAttribute('m'))
            m_cap = int(node.getAttribute('capacity'))
            return m_id, m_mul, m_cap
        return None

    def parse(self) -> PSystem:
        alphabet, rules = self.iterate_rules_node(self._rules)
        membrane_root = self.iterate_scene_node(self._scene_root)
        # membranes = self.__flatten_membrane_tree(membrane_root)
        system = PSystem(alpha=alphabet,
                         rules=rules,
                         membranes=membrane_root,
                         out=membrane_root.id,
                         inference=self._config.inference)
        return system
