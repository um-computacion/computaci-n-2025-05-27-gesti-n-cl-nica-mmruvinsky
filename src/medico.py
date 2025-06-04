from especialidad import Especialidad

class Medico:
    
    def __init__(self, nombre: str, matricula: str, especialidades: list[Especialidad]):
        self.__nombre = nombre
        self.__matricula = matricula
        self.__especialidades = especialidades.copy()


    def obtener_matricula(self) -> str:
        return self.__matricula
    
    def agregar_especialidad(self, especialidad: Especialidad) -> None:
        if especialidad not in self.__especialidades:
            self.__especialidades.append(especialidad)

    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for especialidad in self.__especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None
        

    def __str__(self) -> str:
        return f"Medico: {self.nombre}, Matricula: {self.matricula}, Especialidades: {self.especialidad}"