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