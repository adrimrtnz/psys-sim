from src.utils.parser_factory import SceneParserFactory
from src.utils.config_parser import ConfigParser
from src.classes.move_code_helper import MoveCodeHelper

if __name__ == '__main__':
    config = ConfigParser()
    parser = SceneParserFactory(config)
    root = parser.parse()
    root.print_structure()
