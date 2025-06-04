from typing import List, Dict
from paciente import Paciente
from medico import Medico
from turno import Turno
from historia_clinica import HistoriaClinica

class Clinica:
    def __init__(self, medicos: dict[str, Medico], pacientes: dict[str, Paciente], turnos: list[Turno], historias_clinicas: dict[str, HistoriaClinica]) -> None:
        self.__medicos = medicos
        self.__pacientes = pacientes
        self.__turnos = turnos
        self.__historias_clinicas = historias_clinicas


# AGREGAR


    def agregar_medico(self, medico: Medico) -> None:
        if medico.matricula in self.medicos:
            print(f"El médico con matrícula {medico.matricula} ya está registrado.")
        else:
            self.medicos[medico.matricula] = medico
            print(f"Médico {medico.nombre} agregado correctamente.")

    def agregar_paciente(self, paciente: Paciente) -> None:
        if paciente.dni in self.pacientes:
            print(f"El paciente con DNI {paciente.dni} ya está registrado.")
        else:
            self.pacientes[paciente.dni] = paciente
            print(f"Paciente {paciente.nombre} agregado correctamente.")


# AGENDAR TURNO

    def agendar_turno(self, turno: Turno) -> None:
        if turno.dni_paciente not in self.pacientes:
            print(f"No se puede agendar turno. Paciente con DNI {turno.dni_paciente} no registrado.")
            return
        if turno.matricula_medico not in self.medicos:
            print(f"No se puede agendar turno. Médico con matrícula {turno.matricula} no registrado.")
            return

        self.turnos.append(turno)
        print(f"Turno agendado correctamente para el paciente {turno.dni_paciente} con el médico {turno.matricula_medico}.")


# OBTENER

    def obtener_medicos(self) -> list[Medico]:
        for medico in self.medicos.values():
            print(f"{medico.nombre} | Matrícula: {medico.matricula} | Especialidad: {medico.especialidad}")

    def obtener_pacientes(self) -> list[Paciente]:
        for paciente in self.pacientes.values():
            print(f"{paciente.nombre} | DNI: {paciente.dni} | Edad: {paciente.edad}")
