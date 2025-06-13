import pytest

from src.classes.objects_multiset import ObjectsMultiset

class TestClass:
    obj_a = {'a': 2, 'b': 2}
    obj_b = {'a': 1, 'b': 1}

    def test_and_one(self):
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()

        for o, m in self.obj_a.items():
            ms_1.add(o, m)
            ms_2.add(o, m)
        ms_3 = ms_1 & ms_2
        assert(ms_3.multiset == self.obj_a)

    def test_and_two(self):
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()

        for o, m in self.obj_a.items():
            ms_1.add(o, m)
            
        for o, m in self.obj_b.items():
            ms_2.add(o, m)
        ms_3 = ms_1 & ms_2

        assert(ms_3.multiset == self.obj_b)

    def test_and_three(self):
        ms_1 = ObjectsMultiset()
        with pytest.raises(TypeError):
            ms_1 & 0

    