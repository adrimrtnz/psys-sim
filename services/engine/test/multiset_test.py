import pytest
from src.classes.objects_multiset import ObjectsMultiset


class TestMultisetOperators:
    # Datos de prueba
    obj_a = {'a': 2, 'b': 2}
    obj_b = {'a': 1, 'b': 1}
    obj_c = {'c': 3, 'd': 1}
    obj_mixed = {'a': 3, 'b': 1, 'c': 2}
    
    def test_and_identical_sets(self):
        """Test AND con multisets idénticos"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():
            ms_1.add(o, m)
            ms_2.add(o, m)
        
        ms_3 = ms_1 & ms_2
        assert ms_3.multiset == self.obj_a
    
    def test_and_different_multiplicities(self):
        """Test AND con diferentes multiplicidades - resultado es el mínimo"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():  # {'a': 2, 'b': 2}
            ms_1.add(o, m)
            
        for o, m in self.obj_b.items():  # {'a': 1, 'b': 1}
            ms_2.add(o, m)
        
        ms_3 = ms_1 & ms_2
        assert ms_3.multiset == self.obj_b  # Debería ser el mínimo
    
    def test_and_no_intersection(self):
        """Test AND sin elementos comunes"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():  # {'a': 2, 'b': 2}
            ms_1.add(o, m)
            
        for o, m in self.obj_c.items():  # {'c': 3, 'd': 1}
            ms_2.add(o, m)
        
        ms_3 = ms_1 & ms_2
        assert ms_3.multiset == {}  # Sin elementos comunes
    
    def test_and_partial_intersection(self):
        """Test AND con intersección parcial"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():  # {'a': 2, 'b': 2}
            ms_1.add(o, m)
            
        for o, m in self.obj_mixed.items():  # {'a': 3, 'b': 1, 'c': 2}
            ms_2.add(o, m)
        
        ms_3 = ms_1 & ms_2
        expected = {'a': 2, 'b': 1}  # min(2,3)=2 para 'a', min(2,1)=1 para 'b'
        assert ms_3.multiset == expected
    
    def test_and_empty_multiset(self):
        """Test AND con multiset vacío"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():
            ms_1.add(o, m)
        
        ms_3 = ms_1 & ms_2
        assert ms_3.multiset == {}
    
    def test_and_type_error(self):
        """Test AND con tipo incorrecto"""
        ms_1 = ObjectsMultiset()
        with pytest.raises(TypeError):
            ms_1 & 0
        with pytest.raises(TypeError):
            ms_1 & "string"
        with pytest.raises(TypeError):
            ms_1 & []
    
    # Tests para el operador OR
    def test_or_identical_sets(self):
        """Test OR con multisets idénticos"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():
            ms_1.add(o, m)
            ms_2.add(o, m)
        
        ms_3 = ms_1 | ms_2
        assert ms_3.multiset == self.obj_a
    
    def test_or_different_multiplicities(self):
        """Test OR con diferentes multiplicidades - resultado es el máximo"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():  # {'a': 2, 'b': 2}
            ms_1.add(o, m)
            
        for o, m in self.obj_b.items():  # {'a': 1, 'b': 1}
            ms_2.add(o, m)
        
        ms_3 = ms_1 | ms_2
        assert ms_3.multiset == self.obj_a  # Debería ser el máximo
    
    def test_or_no_intersection(self):
        """Test OR sin elementos comunes - unión completa"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():  # {'a': 2, 'b': 2}
            ms_1.add(o, m)
            
        for o, m in self.obj_c.items():  # {'c': 3, 'd': 1}
            ms_2.add(o, m)
        
        ms_3 = ms_1 | ms_2
        expected = {'a': 2, 'b': 2, 'c': 3, 'd': 1}
        assert ms_3.multiset == expected
    
    def test_or_partial_intersection(self):
        """Test OR con intersección parcial"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():  # {'a': 2, 'b': 2}
            ms_1.add(o, m)
            
        for o, m in self.obj_mixed.items():  # {'a': 3, 'b': 1, 'c': 2}
            ms_2.add(o, m)
        
        ms_3 = ms_1 | ms_2
        expected = {'a': 3, 'b': 2, 'c': 2}  # max(2,3)=3 para 'a', max(2,1)=2 para 'b', 'c' solo en ms_2
        assert ms_3.multiset == expected
    
    def test_or_empty_multiset(self):
        """Test OR con multiset vacío"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():
            ms_1.add(o, m)
        
        ms_3 = ms_1 | ms_2
        assert ms_3.multiset == self.obj_a
        
        # También al revés
        ms_4 = ms_2 | ms_1
        assert ms_4.multiset == self.obj_a
    
    def test_or_both_empty(self):
        """Test OR con ambos multisets vacíos"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        ms_3 = ms_1 | ms_2
        assert ms_3.multiset == {}
    
    def test_or_type_error(self):
        """Test OR con tipo incorrecto"""
        ms_1 = ObjectsMultiset()
        with pytest.raises(TypeError):
            ms_1 | 0
        with pytest.raises(TypeError):
            ms_1 | "string"
        with pytest.raises(TypeError):
            ms_1 | []
    
    # Tests adicionales para casos edge
    def test_operations_with_zero_multiplicities(self):
        """Test para verificar que multiplicidades 0 no se añaden"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        ms_1.add('a', 0)  # Add maneja multiplicidad 0
        ms_2.add('b', 1)
        
        result_and = ms_1 & ms_2
        result_or = ms_1 | ms_2
        
        assert 'a' not in result_and.multiset
        assert 'a' not in result_or.multiset  # Add no debería añadir elementos con multiplicidad 0
    
    def test_commutativity(self):
        """Test para verificar que los operadores son conmutativos"""
        ms_1 = ObjectsMultiset()
        ms_2 = ObjectsMultiset()
        
        for o, m in self.obj_a.items():
            ms_1.add(o, m)
        for o, m in self.obj_mixed.items():
            ms_2.add(o, m)
        
        # AND es conmutativo
        result_and_1 = ms_1 & ms_2
        result_and_2 = ms_2 & ms_1
        assert result_and_1.multiset == result_and_2.multiset
        
        # OR es conmutativo
        result_or_1 = ms_1 | ms_2
        result_or_2 = ms_2 | ms_1
        assert result_or_1.multiset == result_or_2.multiset