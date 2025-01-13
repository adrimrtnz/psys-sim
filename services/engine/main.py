from xml.dom import minidom

from src.utils.xml_parser import XMLInputParser
from src.utils.config_parser import ConfigParser

if __name__ == '__main__':
    config = ConfigParser('../../config/config.ini')
    input_format = config.format
    input_scene  = config.scene
    print(input_format)
    print(input_scene)

    parser = XMLInputParser(input_scene)
    parser.parse()


