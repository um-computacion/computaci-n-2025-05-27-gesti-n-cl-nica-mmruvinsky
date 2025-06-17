import unittest
import sys
import os
from datetime import datetime
from src.historia_clinica import HistoriaClinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from src.turno import Turno
from src.receta import Receta


class TestHistoriaClinica(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.paciente = Paciente("Juan Pérez", "12345678", "01/01/1990")
        self.especialidad = Especialidad("cardiologia", ["lunes", "miercoles"])
        self.medico = Medico("Dr. García", "MN1234", [self.especialidad])
        self.fecha_turno = datetime(2025, 6, 16, 10, 0)
        
    def test_crear_historia_clinica_valida(self):
        historia = HistoriaClinica(self.paciente)
        self.assertEqual(len(historia.obtener_turnos()), 0)
        self.assertEqual(len(historia.obtener_recetas()), 0)
    
    def test_agregar_turno_simple(self):
        historia = HistoriaClinica(self.paciente)
        turno = Turno(self.paciente, self.medico, self.fecha_turno, "cardiologia")
        
        historia.agregar_turno(turno)
        turnos = historia.obtener_turnos()
        
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0], turno)
    
    def test_agregar_multiples_turnos(self):
        historia = HistoriaClinica(self.paciente)
        turno1 = Turno(self.paciente, self.medico, self.fecha_turno, "cardiologia")
        turno2 = Turno(self.paciente, self.medico, datetime(2025, 6, 17, 11, 0), "cardiologia")
        
        historia.agregar_turno(turno1)
        historia.agregar_turno(turno2)
        turnos = historia.obtener_turnos()
        
        self.assertEqual(len(turnos), 2)
        self.assertIn(turno1, turnos)
        self.assertIn(turno2, turnos)
    
    def test_agregar_receta_simple(self):
        historia = HistoriaClinica(self.paciente)
        receta = Receta(self.paciente, self.medico, ["Aspirina"])
        
        historia.agregar_receta(receta)
        recetas = historia.obtener_recetas()
        
        self.assertEqual(len(recetas), 1)
        self.assertEqual(recetas[0], receta)
    
    def test_agregar_multiples_recetas(self):
        historia = HistoriaClinica(self.paciente)
        receta1 = Receta(self.paciente, self.medico, ["Aspirina"])
        receta2 = Receta(self.paciente, self.medico, ["Ibuprofeno", "Paracetamol"])
        
        historia.agregar_receta(receta1)
        historia.agregar_receta(receta2)
        recetas = historia.obtener_recetas()
        
        self.assertEqual(len(recetas), 2)
        self.assertIn(receta1, recetas)
        self.assertIn(receta2, recetas)
    
    def test_obtener_turnos_devuelve_copia(self):
        historia = HistoriaClinica(self.paciente)
        turno = Turno(self.paciente, self.medico, self.fecha_turno, "cardiologia")
        historia.agregar_turno(turno)
        
        turnos = historia.obtener_turnos()
        turnos.clear()  # Modificar la copia
        
        # La historia original no debe verse afectada
        self.assertEqual(len(historia.obtener_turnos()), 1)
    
    def test_obtener_recetas_devuelve_copia(self):
        historia = HistoriaClinica(self.paciente)
        receta = Receta(self.paciente, self.medico, ["Aspirina"])
        historia.agregar_receta(receta)
        
        recetas = historia.obtener_recetas()
        recetas.clear()  # Modificar la copia
        
        # La historia original no debe verse afectada
        self.assertEqual(len(historia.obtener_recetas()), 1)
    
    def test_str_representation_sin_datos(self):
        historia = HistoriaClinica(self.paciente)
        str_historia = str(historia)
        
        self.assertIn("HistoriaClinica", str_historia)
        self.assertIn("Juan Pérez", str_historia)
        self.assertIn("Sin turnos registrados", str_historia)
        self.assertIn("Sin recetas registradas", str_historia)
    
    def test_str_representation_con_datos(self):
        historia = HistoriaClinica(self.paciente)
        turno = Turno(self.paciente, self.medico, self.fecha_turno, "cardiologia")
        receta = Receta(self.paciente, self.medico, ["Aspirina"])
        
        historia.agregar_turno(turno)
        historia.agregar_receta(receta)
        str_historia = str(historia)
        
        self.assertIn("HistoriaClinica", str_historia)
        self.assertIn("Juan Pérez", str_historia)
        self.assertNotIn("Sin turnos registrados", str_historia)
        self.assertNotIn("Sin recetas registradas", str_historia)


if __name__ == '__main__':
    unittest.main()