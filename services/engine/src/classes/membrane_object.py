class MembraneObject:
    def __init__(self, v: str, m: int):
        self._v = v
        self._m = m

    def __str__(self):
        return f'OB - (v={self.value}, mul={self.multiplicity})'

    @property
    def value(self):
        return self._v

    @property
    def multiplicity(self):
        return self._m