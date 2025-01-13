from src.utils.parser_factory import SceneParserFactory
from src.utils.config_parser import ConfigParser

if __name__ == '__main__':
    config = ConfigParser()
    parser = SceneParserFactory(config)
    parser.parse()
