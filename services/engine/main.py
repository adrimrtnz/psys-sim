from src.utils.parser_factory import SceneParserFactory

if __name__ == '__main__':
    parser = SceneParserFactory()
    system = parser.parse()
    
    print('==================== MEMBRANE STRUCTURE ====================')
    system.print_membranes()

    print('\n\n========================== RULES ===========================')
    system.print_rules()
