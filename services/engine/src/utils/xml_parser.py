from xml.dom import minidom
from src.classes.membrane import Membrane
from src.classes.membrane_object import MembraneObject
from src.enums.constants import SceneObjects

class XMLInputParser:
    def __init__(self, scene):
        self._scene = scene
        doc = minidom.parse(f'../../scenes/{scene}.xml')
        self._root = doc.getElementsByTagName('config')[0]

    def iterate_node(self, node, parent : None | Membrane = None ) -> Membrane:
        for child in node.childNodes:
            if child.nodeType == minidom.Node.ELEMENT_NODE:
                attr= self.__get_node_attributes(child)

                if child.nodeName == SceneObjects.MEMBRANE:
                    m_id, m_mul, m_cap = attr
                    membrane = Membrane(m_id, m_mul, m_cap)
                    if parent:
                        parent.add_children(membrane)
                    else:
                        parent = membrane
                    self.iterate_node(child, membrane)
                elif child.nodeName == SceneObjects.OBJECT:
                    bo_v, bo_mul = attr
                    m_object = MembraneObject(v=bo_v, m=bo_mul)
                    parent.add_objects(m_object)   
        return parent

    def __get_node_attributes(self, node):
        if node.nodeName == SceneObjects.OBJECT:
            bo_v = node.getAttribute("v")
            bo_mul = node.getAttribute("m")
            return  bo_v, bo_mul
        if node.nodeName == SceneObjects.MEMBRANE:
            m_id  = node.getAttribute("id")
            m_mul = node.getAttribute("m")
            m_cap = node.getAttribute("capacity")
            return m_id, m_mul, m_cap
        return None

    def parse(self) -> Membrane:
        return self.iterate_node(self._root)

