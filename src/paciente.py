class Paciente:

    def __init__(self, nombre: str, dni: str, fecha_de_nacimiento: str):
        self.__nombre = nombre
        self.__dni = dni
        self.__fecha_de_nacimiento = fecha_de_nacimiento  

    def obtener_dni(self) -> str:
        return self.__dni
    
    def __str__(self) -> str:
        return f"Paciente: {self.__nombre}, DNI: {self.__dni}, Fecha de nacimiento: {self.__fecha_de_nacimiento}"

    