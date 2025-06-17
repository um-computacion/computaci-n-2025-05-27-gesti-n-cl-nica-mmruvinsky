import unittest
import sys
import os
from datetime import datetime
from src.turno import Turno
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad


class TestTurno(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.especialidad = Especialidad("cardiologia", ["lunes", "miercoles"])
        self.medico = Medico("Dr. Juan Perez", "MN1234", [self.especialidad])
        self.paciente = Paciente("Carlos Rodriguez", "12345678", "15/05/1980")
        self.fecha_hora = datetime(2025, 6, 16, 10, 0)  # Lunes 16 de junio 2025, 10:00
    
    def test_crear_turno_valido(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "cardiologia")
        self.assertEqual(turno.obtener_paciente(), self.paciente)
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_hora)
    
    def test_obtener_paciente(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "cardiologia")
        paciente_obtenido = turno.obtener_paciente()
        self.assertEqual(paciente_obtenido, self.paciente)
        self.assertEqual(paciente_obtenido.obtener_dni(), "12345678")
    
    def test_obtener_medico(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "cardiologia")
        medico_obtenido = turno.obtener_medico()
        self.assertEqual(medico_obtenido.obtener_nombre(), "Dr. Juan Perez")
        self.assertEqual(medico_obtenido.obtener_matricula(), "MN1234")
    
    def test_obtener_fecha_hora(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "cardiologia")
        fecha_obtenida = turno.obtener_fecha_hora()
        self.assertEqual(fecha_obtenida, self.fecha_hora)
        self.assertEqual(fecha_obtenida.year, 2025)
        self.assertEqual(fecha_obtenida.month, 6)
        self.assertEqual(fecha_obtenida.day, 16)
    
    def test_str_representation(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "cardiologia")
        str_turno = str(turno)
        self.assertIn("12345678", str_turno)  # DNI del paciente
        self.assertIn("Dr. Juan Perez", str_turno)
        self.assertIn("cardiologia", str_turno)
        self.assertIn("2025-06-16 10:00", str_turno)
    
    def test_turno_con_diferentes_especialidades(self):
        turno1 = Turno(self.paciente, self.medico, self.fecha_hora, "cardiologia")
        
        esp_neurologia = Especialidad("neurologia", ["martes", "jueves"])
        medico2 = Medico("Dra. Ana Lopez", "MP5678", [esp_neurologia])
        fecha2 = datetime(2025, 6, 17, 14, 0)  
        turno2 = Turno(self.paciente, medico2, fecha2, "neurologia")
        
        self.assertNotEqual(turno1.obtener_medico(), turno2.obtener_medico())
        self.assertNotEqual(turno1.obtener_fecha_hora(), turno2.obtener_fecha_hora())
    
    def test_turno_mismo_paciente_diferentes_fechas(self):
        fecha1 = datetime(2025, 6, 16, 10, 0)
        fecha2 = datetime(2025, 6, 18, 15, 0)
        
        turno1 = Turno(self.paciente, self.medico, fecha1, "cardiologia")
        turno2 = Turno(self.paciente, self.medico, fecha2, "cardiologia")
        
        self.assertEqual(turno1.obtener_paciente(), turno2.obtener_paciente())
        self.assertEqual(turno1.obtener_medico(), turno2.obtener_medico())
        self.assertNotEqual(turno1.obtener_fecha_hora(), turno2.obtener_fecha_hora())


if __name__ == '__main__':
    unittest.main()