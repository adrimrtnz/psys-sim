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

    for membrane in config.getElementsByTagName('membrane'):
        m_id  = membrane.getAttribute("id")
        m_mul = membrane.getAttribute("m")
        m_cap = membrane.getAttribute("capacity")

        print(f'Membrane id={m_id} | multiplicity={m_mul} | capacity={m_cap}')



