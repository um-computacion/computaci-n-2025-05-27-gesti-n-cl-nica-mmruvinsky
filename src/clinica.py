from typing import List, Dict
from paciente import Paciente
from medico import Medico
from turno import Turno
from historia_clinica import HistoriaClinica
from datetime import datetime
from receta import Receta

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

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
    
        # VERIFICAR SI EL PACIENTE ESTÁ REGISTRADO EN LA CLINICA
        if not self.validar_existencia_paciente(dni):
            print(f"Paciente con DNI: {dni} no está registrado en la clínica")
            return False
            
        # VERIFICAR SI EL MEDICO ESTA REGISTRADO EN LA CLINICA
        if not self.validar_existencia_medico(matricula):
            print(f"Médico con matrícula: {matricula} no está registrado en la clínica")
            return False
        
        # OBTENER LOS OBJETOS
        paciente = self.obtener_paciente_por_dni(dni) 
        medico = self.obtener_medico_por_matricula(matricula)
        
        # VALIDAR ESPECIALIDAD
        tiene_especialidad = False
        for esp in medico.obtener_especialidades():
            if esp.obtener_especialidad() == especialidad:
                tiene_especialidad = True
                break

        if not tiene_especialidad:
            print(f"El médico no atiende la especialidad {especialidad}")
            return False
        
        #VALIDAR SI EL MEDICO ATIENDE ESA ESPECIALIDAD ESE DIA
        dia_semana = fecha_hora.strftime('%A').lower()
        especialidad_para_dia = medico.obtener_especialidad_para_dia(dia_semana)

        if especialidad_para_dia != especialidad:
            print(f"El médico no atiende {especialidad} los {dia_semana}")
            return False
        
        # VALIDAR TURNO DUPLICADO
        if self.validar_turno_duplicado(matricula, fecha_hora):
            print(f"Ya existe un turno para ese médico en esa fecha y hora")
            return False
        
        # CREAR EL TURNO (después de todas las validaciones)
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        
        # AGREGAR EL TURNO
        self.__turnos.append(turno)
        print(f"Turno agendado correctamente para el paciente {paciente.obtener_nombre()} con el médico {medico.obtener_nombre()}.")
        
        historia = self.obtener_historia_clinica_por_DNI(dni)
        if historia:
            historia.agregar_turno(turno)
        print(f"Turno agregado a la historia clínica del paciente con dni:{dni}")

        return True
    
# EMITIR RECETA

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]) -> str:
        
        # VALIDACIONES BÁSICAS
        if not self.validar_existencia_paciente(dni):
            return f"Error: Paciente con DNI {dni} no está registrado en la clínica"
            
        if not self.validar_existencia_medico(matricula):
            return f"Error: Médico con matrícula {matricula} no está registrado en la clínica"
        
        if not medicamentos:
            return "Error: La receta debe contener al menos un medicamento"
        
        # OBTENER OBJETOS
        paciente = self.obtener_paciente_por_dni(dni)
        medico = self.obtener_medico_por_matricula(matricula)
        
        # CREAR LA RECETA
   
        receta = Receta(paciente, medico, medicamentos)
            
        # AGREGAR A LA HISTORIA CLÍNICA
        historia = self.obtener_historia_clinica_por_DNI(dni)
        if historia:
                historia.agregar_receta(receta)
        else:
                # Crear historia clínica si no existe
                nueva_historia = HistoriaClinica(paciente)
                nueva_historia.agregar_receta(receta)
                self.__historias_clinicas[dni] = nueva_historia
            
        return f"Receta emitida correctamente para {paciente.obtener_nombre()}"
            
# OBTENER

    def obtener_medicos_dict(self) -> dict[str, Medico]:
        return self.__medicos
    
    def obtener_pacientes_dict(self) -> dict[str, Paciente]:
        return self.__pacientes
    
    def obtener_medico_por_matricula(self, matricula: str) -> Medico | None:
        return self.__medicos.get(matricula)
    
    def obtener_paciente_por_dni(self, dni: str) -> Paciente | None:
        return self.__pacientes.get(dni)
    
    def obtener_historia_clinica_por_DNI(self, dni: str) -> HistoriaClinica | None: 
        return self.__historias_clinicas.get(dni) 

    def obtener_turnos(self) -> list[Turno]:  
        return self.__turnos.copy()  
    
    def obtener_pacientes(self) -> list[Paciente]:
        return list(self.__pacientes.values())

    def obtener_medicos(self) -> list[Medico]:
        return list(self.__medicos.values())
        
    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str | None:
        return medico.obtener_especialidad_para_dia(dia_semana)
    
# VALIDAR

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
    
    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        return dias[fecha_hora.weekday()]
    
    

