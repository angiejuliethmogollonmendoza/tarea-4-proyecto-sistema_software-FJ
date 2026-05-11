"""
Módulo de excepciones personalizadas del sistema SoftFJ
"""

# Excepción base del sistema
class SoftFJException(Exception):
    """Excepción base para todo el sistema"""
    pass

# ========== EXCEPCIONES DE CLIENTE ==========
class ClienteException(SoftFJException):
    """Base para errores de cliente"""
    pass

class ClienteNoEncontradoError(ClienteException):
    """Se lanza cuando no se encuentra un cliente"""
    pass

class ClienteYaExisteError(ClienteException):
    """Se lanza cuando intentas crear un cliente duplicado"""
    pass

class DatosClienteInvalidosError(ClienteException):
    """Se lanza cuando los datos del cliente son inválidos"""
    pass

# ========== EXCEPCIONES DE SERVICIO ==========
class ServicioException(SoftFJException):
    """Base para errores de servicio"""
    pass

class ServicioNoDisponibleError(ServicioException):
    """Se lanza cuando un servicio no está disponible"""
    pass

class ServicioNoEncontradoError(ServicioException):
    """Se lanza cuando no se encuentra un servicio"""
    pass

class ParametrosServicioInvalidosError(ServicioException):
    """Se lanza cuando los parámetros son inválidos"""
    pass

# ========== EXCEPCIONES DE RESERVA ==========
class ReservaException(SoftFJException):
    """Base para errores de reserva"""
    pass

class FechaInvalidaError(ReservaException):
    """Se lanza cuando la fecha es inválida (pasada)"""
    pass

class EstadoReservaInvalidoError(ReservaException):
    """Se lanza cuando se intenta cambiar a un estado inválido"""
    pass