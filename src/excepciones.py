class ClinicaException(Exception):
    """Excepción base para errores de la clínica"""
    pass

class PacienteInvalidoException(ClinicaException):
    """Excepción para errores relacionados con datos de pacientes"""
    pass

class MedicoInvalidoException(ClinicaException):
    """Excepción para errores relacionados con datos de médicos"""
    pass

class DNIInvalidoException(PacienteInvalidoException):
    """Excepción específica para DNI inválido"""
    pass

class MatriculaInvalidaException(MedicoInvalidoException):
    """Excepción específica para matrícula inválida"""
    pass

class PacienteNoEncontradoException(PacienteInvalidoException):
    """Excepción para paciente no encontrado"""
    pass

class MedicoNoDisponibleException(MedicoInvalidoException):
    """Excepción para medico no encontrado"""
    pass

class TurnoOcupadoException(ClinicaException):
    """Expepción turno ocupado"""
    pass

class RecetaInvalidaException(ClinicaException):
    """Excepción receta inválida"""
    pass