from xml.dom import minidom

class XMLInputParser:
    def __init__(self, path):
        self._path = path
        doc = minidom.parse(f'../../scenes/{path}.xml')
        self._root = doc.getElementsByTagName('config')[0]

    def iterate_node(self, node, parent=None):
        for hijo in node.childNodes:
            if hijo.nodeType == minidom.Node.ELEMENT_NODE:
                parent_name = parent.nodeName if parent else ''
                m_id  = hijo.getAttribute("id")
                m_mul = hijo.getAttribute("m")
                m_cap = hijo.getAttribute("capacity")
                print(f'Nodo: {hijo.nodeName} | Padre: {parent_name}')
                print(f'    -Membrane id={m_id} | multiplicity={m_mul} | capacity={m_cap}')

                if hijo.hasChildNodes():
                    self.iterate_node(hijo, hijo)

    def parse(self):
        self.iterate_node(self._root)

