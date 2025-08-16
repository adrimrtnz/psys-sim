from src.utils.config_parser import ConfigParser
from src.utils.xml_parser import XMLInputParser

class ParserFactory:
    """A factory for creating input parser instances.

    This class implements the Factory design pattern to abstract and centralize
    the creation logic for input file parsers. Its purpose is to decouple the
    simulation engine from concrete parser implementations (e.g., for XML, JSON),
    thus promoting modularity and making the system easily extensible to
    support new file formats in the future.

    It uses the `__new__` magic method instead of `__init__` to return an
    instance of the appropriate parser class based on the configuration, rather
    than an instance of the factory itself.

    """
    def __new__(cls, config: ConfigParser):
        """Creates and returns a parser instance corresponding to the input format.

        Args:
            config (ConfigParser): A configuration object containing all simulation
                parameters. This object is expected to have a `format` attribute
                that specifies the type of parser to instantiate (e.g., 'xml').

        Returns:
            An instance of a concrete parser capable of processing input files
            of the specified format (e.g., an `XMLInputParser` instance).

        Raises:
            NotImplementedError: If the format specified in the `config` object
                does not correspond to any available parser implementation.
        """
        if config.format == 'xml':
            return XMLInputParser(config)
        raise NotImplementedError(f'Format {config.format} not implemented.')