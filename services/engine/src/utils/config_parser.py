import configparser
from src.enums.constants import InferenceType


class ConfigParser:
    def __init__(self, path: str = '../../config/config.ini'):
        self.parser = configparser.ConfigParser()
        self.parser.read(path)
        self.type_map = {
            None: self.parser.get,
            bool: self.parser.getboolean,
            int: self.parser.getint,
            float: self.parser.getfloat
        }
        self._format = self.__read_field(tag='Input', field='Format', default='xml')
        self._scene  = self.__read_field(tag='Input', field='Scene', default='')
        self._rules  = self.__read_field(tag='Input', field='Rules', default='')
        self._infer  = self.__read_field(tag='Runtime', field='Inference', default=InferenceType.MIN_PARALLEL)
        self._msteps = self.__read_field(tag='Runtime', field='MaxSteps', default=None, dtype=int)

    def __read_field(self, tag: str, field: str, default, dtype: type = None):
        try:
            return self.type_map[dtype](tag, field)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return default

    @property
    def format(self):
        return self._format
    
    @property
    def scene(self):
        return self._scene
    
    @property
    def rules(self):
        return self._rules
    
    @property
    def inference(self):
        return self._infer
    
    @property
    def max_steps(self):
        return self._msteps
