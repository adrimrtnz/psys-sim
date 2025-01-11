from xml.dom import minidom

from src.utils.config_parser import ConfigParser

if __name__ == '__main__':
    config = ConfigParser('../../config/config.ini')
    input_format = config.format
    input_scene  = config.scene
    print(input_format)
    print(input_scene)

    doc = minidom.parse(f'../../scenes/{input_scene}.{input_format}')
    config = doc.getElementsByTagName('config')[0]
    element_nodes = [node for node in config.childNodes if node.nodeType == minidom.Node.ELEMENT_NODE]


    def iterate_node(node, parent=None):
        for hijo in node.childNodes:
            if hijo.nodeType == minidom.Node.ELEMENT_NODE:
                parent_name = parent.nodeName if parent else ''
                m_id  = hijo.getAttribute("id")
                m_mul = hijo.getAttribute("m")
                m_cap = hijo.getAttribute("capacity")
                print(f'Nodo: {hijo.nodeName} | Padre: {parent_name}')
                print(f'    -Membrane id={m_id} | multiplicity={m_mul} | capacity={m_cap}')

                if hijo.hasChildNodes():
                    iterate_node(hijo, hijo)

    iterate_node(config)


