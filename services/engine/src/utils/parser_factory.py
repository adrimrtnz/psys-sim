from src.utils.config_parser import ConfigParser
from src.utils.xml_parser import XMLInputParser

class SceneParserFactory:
    def __new__(cls):
        config = ConfigParser()
        if config.format == 'xml':
            return XMLInputParser(config)
        raise NotImplementedError(f'Format {config.format} not implemented.')