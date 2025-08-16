from collections import deque
from typing import Dict, List, Tuple
from xml.dom import minidom

from src.classes.rule import Rule
from src.classes.rule_dmem import RuleDMEM
from src.classes.objects_multiset import ObjectsMultiset
from src.classes.membrane import Membrane
from src.classes.p_system import PSystem
from src.enums.constants import SceneObject, MoveCode

class XMLInputParser:
    """Parser for XML configuration files defining P-system scenes and rules.

    This class handles the parsing of XML files that define P-system configurations,
    including membrane structures, objects, and evolution rules. It processes both
    scene files (defining the initial membrane structure and objects) and rule files
    (defining the evolution rules for the system).
    """

    def __init__(self, config):

        """Initialize the XMLInputParser with configuration settings.
        
        Args:
            config: Configuration object containing scene and rules file names,
                along with other system parameters like inference settings.
        
        Note:
            The constructor automatically loads and parses the XML files specified
            in the config object. Scene and rules files are expected to be located
            in '../../scenes/' and '../../rules/' directories respectively.
        """
        scene_doc = minidom.parse(f'../../scenes/{config.scene}.xml')
        
        self._config = config
        self._rules = minidom.parse(f'../../rules/{config.rules}.xml')
        self._scene_root = scene_doc.getElementsByTagName('config')[0]

    def iterate_scene_node(self, node, parent : None | Membrane = None ) -> Membrane:
        """Recursively parse scene XML nodes to build the membrane structure.
        
        Traverses the XML scene tree and constructs the corresponding membrane
        hierarchy with their contained objects. Creates parent-child relationships
        between membranes and populates them with their initial object multisets.
        
        Args:
            node: XML node to process (typically the root config node).
            parent: Parent membrane for the current node, None for root membrane.
            
        Returns:
            Membrane: The root membrane of the constructed hierarchy.
            
        Note:
            This method handles both MEMBRANE and OBJECT node types, creating
            the appropriate data structures and relationships between them.
        """
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
        """Parse the rules XML document to extract alphabet, rules, and output configuration.
        
        Processes the rules XML file to extract the system alphabet, evolution rules
        for each membrane, and output configuration. Rules are organized by membrane
        ID and rule type (object rules vs membrane rules).
        
        Args:
            node: XML document containing the rules configuration.
            
        Returns:
            Tuple containing:
                - List[str]: Alphabet of objects used in the system.
                - Dict: Mapping of (membrane_id, rule_type) to lists of Rule objects.
                - Dict: Output configuration specifying which objects to collect.
                
        Note:
            The rules mapping uses tuples of (membrane_id, rule_type) as keys,
            where rule_type is either OBJECT_RULE or MEMBRANE_RULE.
        """
        alphabet = []
        rules_mapping = dict()

        alphabet_node = node.getElementsByTagName('alphabet')[0].getElementsByTagName('v')
        membranes = node.getElementsByTagName('membranes')[0]
        output = self.__get_output_rules(node)

        for item in alphabet_node:
            alphabet.append(item.getAttribute('value'))
        alphabet = tuple(alphabet)

        for membrane in membranes.childNodes:
            if membrane.nodeName == SceneObject.MEMBRANE:
                idx = membrane.getAttribute('id')
                obj_rules = membrane.getElementsByTagName(SceneObject.OBJECT_RULE)
                mem_rules = membrane.getElementsByTagName(SceneObject.MEMBRANE_RULE)
                
                membrane_obj_rules = []
                membrane_mem_rules = []
                for rule in obj_rules:
                    built_rule = self.__build_obj_rule(rule)
                    if not built_rule.idx:
                        built_rule.idx = len(membrane_obj_rules)
                    membrane_obj_rules.append(built_rule)

                for rule in mem_rules:
                    built_rule = self.__build_mem_rule(rule)
                    if not built_rule.idx:
                        built_rule.idx = len(membrane_obj_rules) + len(membrane_mem_rules)
                    membrane_mem_rules.append(built_rule)
                rules_mapping[idx, SceneObject.OBJECT_RULE] = membrane_obj_rules
                rules_mapping[idx, SceneObject.MEMBRANE_RULE] = membrane_mem_rules
        return alphabet, rules_mapping, output
    
    def __get_output_rules(self, node: minidom.Document) -> Dict[str, List[str]] | None:
        """Extract output rules from an XML node.
        
        Args:
            node: XML document containing the output configuration.
            
        Returns:
            Dict with membrane 'id' and list of 'values' or None if no output node is found.
            
        Raises:
            ValueError: If more than one output membrane is specified, as the simulation
                is limited to collecting output from a single membrane.
        """
        try:
            output_node = node.getElementsByTagName('output')[0]
        except IndexError:
            return None
        
        membranes = output_node.getElementsByTagName('membrane')
        if len(membranes) > 1:
            raise ValueError('The simulation is limited to collecting output from a single membrane.')
        output_membrane = membranes[0]
        membrane_id = output_membrane.getAttribute('id')
        output_values = [
            item.getAttribute('value')
            for item in output_membrane.getElementsByTagName('showv')
        ]
        return {'id': membrane_id, 'values': output_values}

    def __build_obj_rule(self, rule_node) -> Rule:
        """Build an object evolution rule from an XML rule node.
        
        Parses an XML object rule node and constructs a Rule object with
        left-hand side objects, right-hand side objects, probability,
        priority, and movement/destination information.
        
        Args:
            rule_node: XML node representing an object evolution rule.
            
        Returns:
            Rule: Constructed rule object with all parsed attributes.
            
        Note:
            If no probability is specified, defaults to 1.0. Movement and
            destination are extracted from the right-hand side if present.
        """
        idx = rule_node.getAttribute('id')
        probability = float(rule_node.getAttribute('pb')) if rule_node.getAttribute('pb') else 1.0
        priority = self.__extract_rule_priority(rule_node=rule_node)
        left_objects, _, _ = self.__extract_rule_objects(rule_node.getElementsByTagName(SceneObject.RULE_LH))
        right_objects, move, dest = self.__extract_rule_objects(rule_node.getElementsByTagName(SceneObject.RULE_RH))
        match move:
            case MoveCode.DMEM.name:
                rule = RuleDMEM(idx=idx,
                            left=left_objects,
                            right=right_objects,
                            prob=probability,
                            prior=priority,
                            move=move)
            case _:
                rule = Rule(idx=idx,
                            left=left_objects,
                            right=right_objects,
                            prob=probability,
                            prior=priority,
                            move=move,
                            destination=dest)
        return rule
    
    def __build_mem_rule(self, rule_node) -> Rule:
        """Build a membrane evolution rule from an XML rule node.
        
        Parses an XML membrane rule node and constructs a Rule object with
        membrane-specific attributes including membrane index for operations
        that affect membrane structure.
        
        Args:
            rule_node: XML node representing a membrane evolution rule.
            
        Returns:
            Rule: Constructed rule object with membrane-specific attributes.
        """
        idx = rule_node.getAttribute('id')
        probability = float(rule_node.getAttribute('pb')) if rule_node.getAttribute('pb') else 1.0
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
        """Extract objects from rule nodes and determine movement/destination.
        
        Parses object nodes within rule definitions to create an ObjectsMultiset
        and extract movement and destination information for the rule.
        
        Args:
            nodes: List of XML nodes containing object definitions.
            
        Returns:
            Tuple containing:
                - ObjectsMultiset: Collection of objects with their multiplicities.
                - str | None: Movement type if specified.
                - str | None: Destination membrane if specified.
                
        Note:
            Returns empty ObjectsMultiset and None values if no nodes are provided.
            Movement and destination are only extracted from right-hand side nodes.
        """
        out = ObjectsMultiset()
        if len(nodes) == 0:
            return out, None, None
        if len(nodes) == 1:
            nodes = nodes[0]
            move = nodes.getAttribute('move') if nodes.nodeName == SceneObject.RULE_RH else None
            objects = nodes.getElementsByTagName(SceneObject.OBJECT)
            dest = nodes.getAttribute('destination') if nodes.hasAttribute('destination') else None
            for obj in objects:
                value = obj.getAttribute('v')
                mult = int(obj.getAttribute('m'))
                out.add_object(value, mult)
            return out, move, dest
        else:
            moves = []
            out = dict()
            for node in nodes:
                move = node.getAttribute('move') if node.nodeName == SceneObject.RULE_RH else None
                out[move] = list()
                objects = node.getElementsByTagName(SceneObject.OBJECT)
                dest = node.getAttribute('destination') if node.hasAttribute('destination') else MoveCode.HERE.name
                moves.append(move)
                for obj in objects:
                    value = obj.getAttribute('v')
                    mult = int(obj.getAttribute('m'))
                    out[move].append((value, mult, dest))

            if MoveCode.DMEM.name in moves:
                move = MoveCode.DMEM.name
            else:
                raise ValueError(f'Not handled rule extraction for moves {moves}.')
            return out, move, dest
    
    def __extract_rule_membrane_objects(self, nodes) -> Tuple[Dict, str | None]:
        """Extract objects and membrane information from membrane rule nodes.
        
        Specialized extraction method for membrane rules that includes membrane
        index information in addition to the standard object extraction.
        
        Args:
            nodes: List of XML nodes containing membrane rule definitions.
            
        Returns:
            Tuple containing:
                - ObjectsMultiset: Collection of objects with their multiplicities.
                - str | None: Movement type if specified.
                - str | None: Destination membrane if specified.
                - str: Membrane index for the rule operation.
                
        Note:
            Returns empty dict and None values if no nodes are provided.
            The membrane index is extracted from the MEMwOB element.
        """
        if len(nodes) == 0:
            return dict(), None, None
        mem_idx = nodes[0].getElementsByTagName('MEMwOB')[0].getAttribute('id')
        return *self.__extract_rule_objects(nodes), mem_idx
    
    def __extract_rule_priority(self, rule_node):
        """Extracts and parses the priority of a rule from its XML node.

        This method reads the 'pr' attribute, which defines a rule's priority
        over other rules. Priority is used to resolve conflicts when multiple
        rules are applicable in the same simulation step. The attribute value is
        expected to be a comma-separated string of other rule IDs.

        A rule cannot have a priority defined for it if it does not also have
        a unique 'id' attribute.

        Args:
            rule_node (Element): The XML element representing a single rule,
                from which to extract the priority.

        Returns:
            Optional[List[str]]: A list of rule IDs that this rule takes
            priority over. Returns None if the 'pr' attribute is not specified.

        Raises:
            ValueError: If the 'pr' attribute is present but the rule's 'id'
                attribute is missing or empty.
        """
        idx = rule_node.getAttribute('id')
        priority = rule_node.getAttribute('pr')
        if priority and not idx:
            error_message = (
                f"Invalid rule configuration: A rule with a priority attribute ('pr'=\"{priority}\") "
                f"must also have a non-empty 'id' attribute. Please add an 'id' to this rule."
            )
            raise ValueError(error_message)
        if priority:
            return [prior.strip() for prior in priority.split(',')]
        return None

    @staticmethod
    def __get_node_attributes(node) -> List[str] | None:
        """Extract attributes from XML nodes based on node type.
        
        Static method that parses XML node attributes and returns them in
        the appropriate format based on whether the node represents an
        object or a membrane.
        
        Args:
            node: XML node to extract attributes from.
            
        Returns:
            List containing:
                - For OBJECT nodes: [value, multiplicity]
                - For MEMBRANE nodes: [id, multiplicity, capacity]
                - None for unrecognized node types.
                
        Note:
            Multiplicity and capacity values are converted to integers,
            while IDs and values remain as strings.
        """
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
        """Parse the loaded XML files and construct a complete P-system.
        
        Main parsing method that orchestrates the extraction of all system
        components from the loaded XML files and constructs a complete
        PSystem object ready for simulation.
        
        Returns:
            PSystem: object containing alphabet, rules, membrane structure,
            output configuration, and inference settings.
                
        Note:
            This method combines the results from scene and rules parsing to
            create a unified system representation.
        """
        alphabet, rules, output = self.iterate_rules_node(self._rules)
        membrane_root = self.iterate_scene_node(self._scene_root)
        system = PSystem(alpha=alphabet,
                         rules=rules,
                         membranes=membrane_root,
                         out=output,
                         inference=self._config.inference)
        return system
