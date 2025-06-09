from typing import List, Dict
from paciente import Paciente
from medico import Medico
from turno import Turno
from historia_clinica import HistoriaClinica
from datetime import datetime

class Clinica:
    def __init__(self, medicos: dict[str, Medico], pacientes: dict[str, Paciente], turnos: list[Turno], historias_clinicas: dict[str, HistoriaClinica]) -> None:
        self.__medicos = medicos
        self.__pacientes = pacientes
        self.__turnos = turnos
        self.__historias_clinicas = historias_clinicas


# AGREGAR

    def agregar_medico(self, medico: Medico) -> None:
        if medico.obtener_matricula() in self.__medicos:
            print(f"El médico con matrícula {medico.obtener_matricula()} ya está registrado.")
        else:
            self.__medicos[medico.obtener_matricula()] = medico
            print(f"Médico {medico.obtener_nombre()} agregado correctamente.")


    def agregar_paciente(self, paciente: Paciente) -> None:
        if paciente.obtener_dni() in self.__pacientes:
            print(f"El paciente con DNI {paciente.obtener_dni()} ya está registrado.")
        else:
            self.__pacientes[paciente.obtener_dni()] = paciente
            print(f"Paciente {paciente.obtener_nombre()} agregado correctamente.")



# AGENDAR TURNO

    def agendar_turno(self, turno: Turno) -> None:

        paciente = turno.obtener_paciente()
        medico = turno.obtener_medico()
        
        dni_paciente = paciente.obtener_dni()
        matricula_medico = medico.obtener_matricula()
        
        # VERIFICAR SI EL PACIENTE ESTÁ REGISTRADO EN LA CLINICA
        if dni_paciente not in self.__pacientes:
            print(f"No se puede agendar turno. Paciente con DNI {dni_paciente} no registrado.")
            return
            
        # VERIFICAR SI EL MEDICO ESTA REGISTRADO EN LA CLINICA
        if matricula_medico not in self.__medicos:
            print(f"No se puede agendar turno. Médico con matrícula {matricula_medico} no registrado.")
            return

        self.__turnos.append(turno)
        print(f"Turno agendado correctamente para el paciente {paciente.obtener_nombre()} con el médico {medico.obtener_nombre()}.")


# OBTENER

    def obtener_medicos_dict(self) -> dict[str, Medico]:
        return self.__medicos
    
    def obtener_pacientes_dict(self) -> dict[str, Paciente]:
        return self.__pacientes
    
    def obtener_medico_por_matricula(self, matricula: str) -> Medico | None:
        return self.__medicos.get(matricula)
    
    def obtener_historia_clinica_por_DNI(self, dni: str) -> HistoriaClinica | None: 
        return self.__historias_clinicas.get(dni) 
     
    def obtener_turnos(self, turnos: list[Turno]):
        return self.__turnos
    
# VALIDACIONES

    def validar_existencia_paciente(self, dni: str) -> bool:
        if dni in self.__pacientes:
            return True
        else:
            return False
        
    def validar_existencia_medico(self, matricula: str) -> bool:
        if matricula in self.__medicos:
            return True
        else:
            return False
        
    def validar_turno_duplicado(self, matricula: str, fecha_hora: datetime) -> bool:
        for turno in self.__turnos:
            if (turno.obtener_medico().obtener_matricula() == matricula and 
                turno.obtener_fecha_hora() == fecha_hora):
                return True     
        return False 
    
    

