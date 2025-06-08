from src.utils.config_parser import ConfigParser
from src.utils.parser_factory import SceneParserFactory

if __name__ == '__main__':
    config = ConfigParser()
    parser = SceneParserFactory(config)
    system = parser.parse()
    
    print('==================== MEMBRANE STRUCTURE ====================')
    system.print_membranes()

    print('\n\n========================== RULES ===========================')
    system.print_rules()
    system.run(config.max_steps)

    print('==================== MEMBRANE STRUCTURE ====================')
    # system.print_membranes()
