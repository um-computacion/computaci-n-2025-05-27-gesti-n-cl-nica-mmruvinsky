import re
from src.excepciones import ( DNIInvalidoException, PacienteInvalidoException ) 

class Paciente:

    def __init__(self, nombre: str, dni: str, fecha_de_nacimiento: str):
        self.__nombre = self._validar_nombre(nombre)  
        self.__dni = self._validar_dni(dni)
        self.__fecha_de_nacimiento = fecha_de_nacimiento  

# VALIDACIONES

    def _validar_nombre(self, nombre: str) -> str:
        if not nombre:
            raise PacienteInvalidoException("El nombre del paciente no puede estar vacío")
        
        nombre_limpio = nombre.strip()
        
        if not nombre_limpio:
            raise PacienteInvalidoException("El nombre del paciente no puede estar vacío")
        
        return nombre_limpio  

    def _validar_dni(self, dni: str) -> str:
 
        if not dni:
            raise DNIInvalidoException("El DNI no puede estar vacío")
        
        dni_limpio = re.sub(r'[.\s]', '', dni)
        patron_dni = r'^\d{7,8}$'
        
        if not re.match(patron_dni, dni_limpio):
            raise DNIInvalidoException("DNI inválido. Debe tener 7-8 dígitos")
        
        return dni_limpio

# GETTERS

    def obtener_nombre(self) -> str:
        return self.__nombre

    def obtener_dni(self) -> str:
        return self.__dni
    
    def __str__(self) -> str:
        return f"Paciente: {self.__nombre}, DNI: {self.__dni}, Fecha de nacimiento: {self.__fecha_de_nacimiento}"