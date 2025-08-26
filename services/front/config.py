from typing import Dict, Union

class Config:

    def __init__(self, config: Union[Dict, None] = None):
        self._config = config if config is not None else dict()

    @property
    def format(self):
        return self._config.get('format', 'xml')

    @format.setter
    def format(self, value):
        self._config['format'] = value

    @property
    def scene(self):
        return self._config.get('scene', None)

    @scene.setter
    def scene(self, value):
        self._config['scene'] = value

    @property
    def rules(self):
        return self._config.get('rules', None)

    @rules.setter
    def rules(self, value):
        self._config['rules'] = value

    @property
    def inference(self):
        return self._config.get('inference', 'maxpar')

    @inference.setter
    def inference(self, value):
        self._config['inference'] = value

    @property
    def max_steps(self):
        return self._config.get('max_steps', None)

    @max_steps.setter
    def max_steps(self, value):
        self._config['max_steps'] = value

    @property
    def seed(self):
        return self._config.get('seed', None)

    @seed.setter
    def seed(self, value):
        self._config['seed'] = value
