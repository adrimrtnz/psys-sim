from src.utils.config_parser import ConfigParser


if __name__ == '__main__':
    config = ConfigParser('../../config/config.ini')
    input_format = config.format
    print(input_format)
