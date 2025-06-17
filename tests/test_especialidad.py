import unittest
import sys
import os
from src.especialidad import Especialidad


class TestEspecialidad(unittest.TestCase):
    
    def test_crear_especialidad_valida(self):
        especialidad = Especialidad("cardiologia", ["lunes", "miercoles"])
        self.assertEqual(especialidad.obtener_especialidad(), "cardiologia")
    
    def test_verificar_dia_existente(self):
        especialidad = Especialidad("cardiologia", ["lunes", "miercoles"])
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertTrue(especialidad.verificar_dia("miercoles"))
    
    def test_verificar_dia_no_existente(self):
        especialidad = Especialidad("cardiologia", ["lunes", "miercoles"])
        self.assertFalse(especialidad.verificar_dia("martes"))
        self.assertFalse(especialidad.verificar_dia("viernes"))
    
    def test_dias_case_insensitive(self):
        especialidad = Especialidad("cardiologia", ["Lunes", "MIERCOLES"])
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertTrue(especialidad.verificar_dia("LUNES"))
        self.assertTrue(especialidad.verificar_dia("miercoles"))
        self.assertTrue(especialidad.verificar_dia("MIERCOLES"))
    
    def test_verificar_dia_case_insensitive(self):
        especialidad = Especialidad("cardiologia", ["lunes", "miercoles"])
        self.assertTrue(especialidad.verificar_dia("LUNES"))
        self.assertTrue(especialidad.verificar_dia("Miercoles"))
    
    def test_especialidad_sin_dias(self):
        especialidad = Especialidad("cardiologia", [])
        self.assertFalse(especialidad.verificar_dia("lunes"))
    
    def test_str_representation(self):
        especialidad = Especialidad("cardiologia", ["lunes", "miercoles"])
        expected = "Tipo de especialidad: cardiologia, Días: ['lunes', 'miercoles']"
        self.assertEqual(str(especialidad), expected)
    

if __name__ == '__main__':
    unittest.main()