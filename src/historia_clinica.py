from src.turno import Turno
from src.paciente import Paciente
from src.receta import Receta

class HistoriaClinica:

    def __init__(self, paciente: Paciente):
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []

# OBTENER

    def obtener_turnos(self) -> list[Turno]:
        return self.__turnos.copy()

    def obtener_recetas(self) -> list[Receta]:
        return self.__recetas.copy()

# AGREGAR

    def agregar_turno(self, turno: Turno) -> None:
        self.__turnos.append(turno)

    def agregar_receta(self, receta: Receta) -> None:
        self.__recetas.append(receta)

    def __str__(self) -> str:
        turnos_str = "\n    ".join(str(t) for t in self.__turnos) or "Sin turnos registrados"
        recetas_str = "\n    ".join(str(r) for r in self.__recetas) or "Sin recetas registradas"

        return (
            f"HistoriaClinica(\n"
            f"  Paciente: {self.__paciente},\n"
            f"  Turnos:\n    {turnos_str},\n"
            f"  Recetas:\n    {recetas_str}\n"
            f")"
        )
