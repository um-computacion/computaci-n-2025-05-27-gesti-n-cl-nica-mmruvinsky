from src.paciente import Paciente
from src.medico import Medico
from src.excepciones import RecetaInvalidaException
from datetime import datetime

class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):
        if not medicamentos:
            raise ValueError("La receta debe contener al menos un medicamento.")

        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = medicamentos
        self.__fecha = datetime.now()

    def __str__(self) -> str:
        medicamentos_str = ", ".join(self.__medicamentos)
        fecha_str = self.__fecha.strftime("%d/%m/%Y")
        return f"Receta: Paciente: {self.__paciente}, Médico: {self.__medico}, Medicamentos: [{medicamentos_str}], Fecha: {fecha_str}  "


     