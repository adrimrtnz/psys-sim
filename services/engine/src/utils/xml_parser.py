from xml.dom import minidom

class XMLInputParser:
    def __init__(self, scene):
        self._scene = scene
        doc = minidom.parse(f'../../scenes/{scene}.xml')
        self._root = doc.getElementsByTagName('config')[0]

    def iterate_node(self, node, parent=None):
        for child in node.childNodes:
            if child.nodeType == minidom.Node.ELEMENT_NODE:
                parent_name = parent.nodeName if parent else ''
                m_id  = child.getAttribute("id")
                m_mul = child.getAttribute("m")
                m_cap = child.getAttribute("capacity")
                print(f'Nodo: {child.nodeName} | Padre: {parent_name}')
                print(f'    -Membrane id={m_id} | multiplicity={m_mul} | capacity={m_cap}')

                if child.hasChildNodes():
                    self.iterate_node(child, child)

    def parse(self):
        self.iterate_node(self._root)

