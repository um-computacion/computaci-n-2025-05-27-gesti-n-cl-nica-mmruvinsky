from especialidad import Especialidad
import re
from excepciones import (
    MedicoInvalidoException,
    MatriculaInvalidaException
)

class Medico:
    
    def __init__(self, nombre: str, matricula: str, especialidades: list[Especialidad]):
        self.__nombre = nombre
        self.__matricula = matricula
        self.__especialidades = especialidades.copy()

# GETTERS

    def obtener_matricula(self) -> str:
        return self.__matricula
    
    def obtener_nombre(self) -> str:
        return self.__nombre
    
    def obtener_especialidades(self) -> list[Especialidad]:
        return self.__especialidades.copy()
    
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for especialidad in self.__especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None
    
# AGREGAR
    
    def agregar_especialidad(self, especialidad: Especialidad) -> None:
        if especialidad not in self.__especialidades:
            self.__especialidades.append(especialidad)

    def _validar_matricula(self, matricula: str) -> str:

        if not matricula:
            raise MatriculaInvalidaException("La matrícula no puede estar vacía")
        
        matricula_limpia = matricula.strip().upper()
        patron_matricula = r'^M[NP]\d{4,6}$'
        
        if not re.match(patron_matricula, matricula_limpia):
            raise MatriculaInvalidaException("Matrícula inválida. Formato: MN##### o MP##### (4-6 dígitos)")
        
        return matricula_limpia
       
    def __str__(self) -> str:
        return f"Medico: {self.__nombre}, Matricula: {self.__matricula}, Especialidades: {self.__especialidades}"