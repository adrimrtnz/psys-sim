import configparser

default_values = {
    'Input': {
        'Format': 'json'
    }
}

class ConfigParser:
    def __init__(self, path: str):
        self.parser = configparser.ConfigParser()
        self.parser.read(path)
        self.type_map = {
            str: self.parser.get,
            bool: self.parser.getboolean,
            int: self.parser.getint,
            float: self.parser.getfloat
        }
        self._format = self.get_field(tag='Input', field='Format', dtype=str)

    def get_field(self, tag: str, field: str, dtype: type = str):
        try:
            value = self.type_map[dtype](tag, field)
            return value
        except configparser.NoSectionError:
            return default_values[tag][field]

    @property
    def format(self):
        return self._format
