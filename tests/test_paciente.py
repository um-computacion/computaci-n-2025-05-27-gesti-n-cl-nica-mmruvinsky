import unittest
import sys
import os
from src.paciente import Paciente
from src.excepciones import ( DNIInvalidoException, PacienteInvalidoException )


class TestPaciente(unittest.TestCase):
    
    def test_crear_paciente_valido(self):
        paciente = Paciente("Juan Pérez", "12345678", "01/01/1990")
        self.assertEqual(paciente.obtener_nombre(), "Juan Pérez")
        self.assertEqual(paciente.obtener_dni(), "12345678")
    
    def test_crear_paciente_nombre_vacio(self):
        with self.assertRaises(PacienteInvalidoException):
            Paciente("", "12345678", "01/01/1990")
    
    def test_dni_con_puntos_y_espacios(self):
        paciente = Paciente("Test", "12. 345. 678", "01/01/1990")
        self.assertEqual(paciente.obtener_dni(), "12345678")
    
    def test_dni_con_espacios(self):
        paciente = Paciente("Test", "12 345 678", "01/01/1990")
        self.assertEqual(paciente.obtener_dni(), "12345678")
    
    def test_dni_con_puntos(self):
        paciente = Paciente("Test", "12.345.678", "01/01/1990")
        self.assertEqual(paciente.obtener_dni(), "12345678")
    
    def test_dni_vacio_error(self):
        with self.assertRaises(DNIInvalidoException):
            Paciente("Test", "", "01/01/1990")
    
    def test_dni_muy_corto_error(self):
        with self.assertRaises(DNIInvalidoException):
            Paciente("Test", "1234", "01/01/1990")
    
    def test_dni_muy_largo_error(self):
        with self.assertRaises(DNIInvalidoException):
            Paciente("Test", "123456789", "01/01/1990")
    
    def test_dni_con_letras_error(self):
        with self.assertRaises(DNIInvalidoException):
            Paciente("Test", "1234567A", "01/01/1990")
    
    def test_str_representation(self):
        paciente = Paciente("Juan Pérez", "12345678", "01/01/1990")
        expected = "Paciente: Juan Pérez, DNI: 12345678, Fecha de nacimiento: 01/01/1990"
        self.assertEqual(str(paciente), expected)


if __name__ == '__main__':
    unittest.main()