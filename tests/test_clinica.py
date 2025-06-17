import unittest
import sys
import os
from datetime import datetime
from src.clinica import Clinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from src.historia_clinica import HistoriaClinica
from src.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    TurnoOcupadoException,
    RecetaInvalidaException
)


class TestClinica(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear especialidades
        self.esp_cardiologia = Especialidad("cardiologia", ["lunes", "miercoles"])
        self.esp_neurologia = Especialidad("neurologia", ["martes", "jueves"])
        
        # Crear médicos
        self.medico1 = Medico("Dr. Juan Perez", "MN1234", [self.esp_cardiologia])
        self.medico2 = Medico("Dra. Ana Lopez", "MP5678", [self.esp_neurologia])
        
        # Crear pacientes
        self.paciente1 = Paciente("Carlos Rodriguez", "12345678", "15/05/1980")
        self.paciente2 = Paciente("Maria Gonzalez", "87654321", "20/10/1975")
        
        # Crear historia clínica
        self.historia1 = HistoriaClinica(self.paciente1)
        
        # Crear clínica
        self.clinica = Clinica(
            medicos={"MN1234": self.medico1, "MP5678": self.medico2},
            pacientes={"12345678": self.paciente1, "87654321": self.paciente2},
            turnos=[],
            historias_clinicas={"12345678": self.historia1}
        )

    # ===== TESTS AGREGAR MÉDICO =====
    
    def test_agregar_medico_nuevo(self):
        """Test agregar médico nuevo"""
        nuevo_medico = Medico("Dr. Luis Martinez", "MN9999", [self.esp_cardiologia])
        self.clinica.agregar_medico(nuevo_medico)
        
        medicos = self.clinica.obtener_medicos_dict()
        self.assertIn("MN9999", medicos)
        self.assertEqual(medicos["MN9999"], nuevo_medico)

    def test_agregar_medico_existente(self):
        """Test agregar médico con matrícula existente"""
        medico_duplicado = Medico("Dr. Otro Nombre", "MN1234", [self.esp_neurologia])
        self.clinica.agregar_medico(medico_duplicado)
        
        # Verificar que no se sobrescribió
        medicos = self.clinica.obtener_medicos_dict()
        self.assertEqual(medicos["MN1234"].obtener_nombre(), "Dr. Juan Perez")

    # ===== TESTS AGREGAR PACIENTE =====
    
    def test_agregar_paciente_nuevo(self):
        """Test agregar paciente nuevo"""
        nuevo_paciente = Paciente("Pedro Sanchez", "11111111", "10/01/1990")
        self.clinica.agregar_paciente(nuevo_paciente)
        
        pacientes = self.clinica.obtener_pacientes_dict()
        self.assertIn("11111111", pacientes)
        self.assertEqual(pacientes["11111111"], nuevo_paciente)

    def test_agregar_paciente_existente(self):
        """Test agregar paciente con DNI existente"""
        paciente_duplicado = Paciente("Otro Nombre", "12345678", "01/01/2000")
        self.clinica.agregar_paciente(paciente_duplicado)
        
        # Verificar que no se sobrescribió
        pacientes = self.clinica.obtener_pacientes_dict()
        self.assertEqual(pacientes["12345678"].obtener_nombre(), "Carlos Rodriguez")

    # ===== TESTS AGENDAR TURNO =====
    
    def test_agendar_turno_exitoso(self):
        """Test agendar turno exitosamente"""
        # Lunes - día que el médico atiende cardiología
        fecha_turno = datetime(2025, 6, 16, 10, 0)  # 16 jun 2025 es lunes
        
        resultado = self.clinica.agendar_turno("12345678", "MN1234", "cardiologia", fecha_turno)
        
        self.assertTrue(resultado)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)

    def test_agendar_turno_paciente_no_registrado(self):
        """Test agendar turno con paciente no registrado"""
        fecha_turno = datetime(2025, 6, 16, 10, 0)
        
        resultado = self.clinica.agendar_turno("99999999", "MN1234", "cardiologia", fecha_turno)
        
        self.assertFalse(resultado)
        self.assertEqual(len(self.clinica.obtener_turnos()), 0)

    def test_agendar_turno_medico_no_registrado(self):
        """Test agendar turno con médico no registrado"""
        fecha_turno = datetime(2025, 6, 16, 10, 0)
        
        resultado = self.clinica.agendar_turno("12345678", "MN9999", "cardiologia", fecha_turno)
        
        self.assertFalse(resultado)
        self.assertEqual(len(self.clinica.obtener_turnos()), 0)

    def test_agendar_turno_especialidad_no_disponible(self):
        """Test agendar turno con especialidad que el médico no tiene"""
        fecha_turno = datetime(2025, 6, 16, 10, 0)
        
        resultado = self.clinica.agendar_turno("12345678", "MN1234", "neurologia", fecha_turno)
        
        self.assertFalse(resultado)

    def test_agendar_turno_dia_no_disponible(self):
        """Test agendar turno en día que el médico no atiende esa especialidad"""
        # Viernes - día que el médico NO atiende cardiología
        fecha_turno = datetime(2025, 6, 20, 10, 0)  # 20 jun 2025 es viernes
        
        resultado = self.clinica.agendar_turno("12345678", "MN1234", "cardiologia", fecha_turno)
        
        self.assertFalse(resultado)

    def test_agendar_turno_duplicado(self):
        """Test agendar turno en horario ya ocupado"""
        fecha_turno = datetime(2025, 6, 16, 10, 0)  # Lunes
        
        # Agendar primer turno
        resultado1 = self.clinica.agendar_turno("12345678", "MN1234", "cardiologia", fecha_turno)
        self.assertTrue(resultado1)
        
        # Intentar agendar segundo turno en misma fecha/hora
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("87654321", "MN1234", "cardiologia", fecha_turno)

    # ===== TESTS EMITIR RECETA =====
    
    def test_emitir_receta_exitoso(self):
        """Test emitir receta exitosamente"""
        medicamentos = ["Aspirina", "Ibuprofeno"]
        
        resultado = self.clinica.emitir_receta("12345678", "MN1234", medicamentos)
        
        self.assertEqual(resultado, "Receta emitida correctamente para Carlos Rodriguez")

    def test_emitir_receta_paciente_no_encontrado(self):
        """Test emitir receta con paciente no encontrado"""
        medicamentos = ["Aspirina"]
        
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("99999999", "MN1234", medicamentos)

    def test_emitir_receta_medico_no_encontrado(self):
        """Test emitir receta con médico no encontrado"""
        medicamentos = ["Aspirina"]
        
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "MN9999", medicamentos)

    def test_emitir_receta_sin_medicamentos(self):
        """Test emitir receta sin medicamentos"""
        medicamentos = []
        
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "MN1234", medicamentos)

    # ===== TESTS OBTENER MÉTODOS =====
    
    def test_obtener_medico_por_matricula_existente(self):
        """Test obtener médico existente por matrícula"""
        medico = self.clinica.obtener_medico_por_matricula("MN1234")
        self.assertEqual(medico, self.medico1)
        self.assertEqual(medico.obtener_nombre(), "Dr. Juan Perez")

    def test_obtener_medico_por_matricula_no_existente(self):
        """Test obtener médico no existente por matrícula"""
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("MN9999")

    def test_obtener_paciente_por_dni_existente(self):
        """Test obtener paciente existente por DNI"""
        paciente = self.clinica.obtener_paciente_por_dni("12345678")
        self.assertEqual(paciente, self.paciente1)
        self.assertEqual(paciente.obtener_nombre(), "Carlos Rodriguez")

    def test_obtener_paciente_por_dni_no_existente(self):
        """Test obtener paciente no existente por DNI"""
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_paciente_por_dni("99999999")

    def test_obtener_historia_clinica_existente(self):
        """Test obtener historia clínica existente"""
        historia = self.clinica.obtener_historia_clinica_por_DNI("12345678")
        self.assertIsNotNone(historia)

    def test_obtener_historia_clinica_no_existente(self):
        """Test obtener historia clínica no existente"""
        historia = self.clinica.obtener_historia_clinica_por_DNI("99999999")
        self.assertIsNone(historia)

    def test_obtener_turnos(self):
        """Test obtener lista de turnos"""
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 0)
        self.assertIsInstance(turnos, list)

    def test_obtener_pacientes(self):
        """Test obtener lista de pacientes"""
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 2)
        self.assertIn(self.paciente1, pacientes)
        self.assertIn(self.paciente2, pacientes)

    def test_obtener_medicos(self):
        """Test obtener lista de médicos"""
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 2)
        self.assertIn(self.medico1, medicos)
        self.assertIn(self.medico2, medicos)

    # ===== TESTS VALIDAR MÉTODOS =====
    
    def test_validar_existencia_paciente_existente(self):
        """Test validar existencia de paciente existente"""
        resultado = self.clinica.validar_existencia_paciente("12345678")
        self.assertTrue(resultado)

    def test_validar_existencia_paciente_no_existente(self):
        """Test validar existencia de paciente no existente"""
        resultado = self.clinica.validar_existencia_paciente("99999999")
        self.assertFalse(resultado)

    def test_validar_existencia_medico_existente(self):
        """Test validar existencia de médico existente"""
        resultado = self.clinica.validar_existencia_medico("MN1234")
        self.assertTrue(resultado)

    def test_validar_existencia_medico_no_existente(self):
        """Test validar existencia de médico no existente"""
        resultado = self.clinica.validar_existencia_medico("MN9999")
        self.assertFalse(resultado)

    def test_obtener_dia_semana_en_espanol(self):
        """Test obtener día de la semana en español"""
        # Lunes 16 de junio de 2025
        fecha = datetime(2025, 6, 16)
        resultado = self.clinica.obtener_dia_semana_en_espanol(fecha)
        self.assertEqual(resultado, "lunes")
        
        # Viernes 20 de junio de 2025
        fecha = datetime(2025, 6, 20)
        resultado = self.clinica.obtener_dia_semana_en_espanol(fecha)
        self.assertEqual(resultado, "viernes")


if __name__ == '__main__':
    unittest.main()