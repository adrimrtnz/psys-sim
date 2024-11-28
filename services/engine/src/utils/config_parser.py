import configparser


class ConfigParser:
    def __init__(self, path: str):
        self.parser = configparser.ConfigParser()
        self.parser.read(path)
        self.type_map = {
            None: self.parser.get,
            bool: self.parser.getboolean,
            int: self.parser.getint,
            float: self.parser.getfloat
        }
        self._format = self.__read_field(tag='Input', field='Format', default='json')

    def __read_field(self, tag: str, field: str, default, dtype: type = None):
        try:
            return self.type_map[dtype](tag, field)
        except configparser.NoOptionError | configparser.NoSectionError:
            return default

    @property
    def format(self):
        return self._format
