from src.utils.xml_parser import XMLInputParser

class SceneParserFactory:
    def __new__(cls, config):
        if config.format == 'xml':
            return XMLInputParser(config.scene, config.rules)
        raise NotImplementedError(f'Format {config.format} not implemented.')