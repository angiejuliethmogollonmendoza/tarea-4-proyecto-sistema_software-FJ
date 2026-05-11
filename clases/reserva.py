"""
Clase Reserva - Integra cliente, servicio y gestiona el estado
"""

from datetime import datetime
from .entidad import Entidad
from .excepciones import FechaInvalidaError, EstadoReservaInvalidoError, ServicioNoDisponibleError

class Reserva(Entidad):
    """
    Representa una reserva que asocia un cliente con un servicio
    """
    
    ESTADOS_VALIDOS = ["pendiente", "confirmada", "cancelada", "completada"]
    
    def __init__(self, id_reserva: str, cliente, servicio, fecha_inicio: datetime, duracion_horas: float):
        """
        Crea una nueva reserva
        
        Args:
            id_reserva: Identificador único
            cliente: Objeto Cliente
            servicio: Objeto Servicio (cualquier tipo)
            fecha_inicio: Fecha y hora de inicio
            duracion_horas: Duración en horas
        """
        super().__init__(id_reserva)
        self._cliente = cliente
        self._servicio = servicio
        self._fecha_inicio = fecha_inicio
        self._duracion_horas = duracion_horas
        self._estado = "pendiente"
        self._costo_total = None
        
        # Validaciones iniciales
        self._validar_fecha()
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible")
    
    # ========== PROPIEDADES ==========
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def servicio(self):
        return self._servicio
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def costo_total(self):
        return self._costo_total
    
    @property
    def fecha_inicio(self):
        return self._fecha_inicio
    
    # ========== MÉTODOS PRIVADOS ==========
    def _validar_fecha(self):
        """Valida que la fecha no sea pasada"""
        if self._fecha_inicio < datetime.now():
            raise FechaInvalidaError("No se pueden hacer reservas en fechas pasadas")
    
    def _calcular_costo(self):
        """
        Llama al método polimórfico del servicio para calcular el costo
        """
        nombre_servicio = type(self._servicio).__name__
        
        # Parámetros específicos según el tipo de servicio
        if nombre_servicio == "ReservaSala":
            self._costo_total = self._servicio.calcular_costo(
                horas=self._duracion_horas, 
                tipo_sala="ejecutiva"
            )
        elif nombre_servicio == "AlquilerEquipo":
            # Convertir horas a días (aproximación)
            dias = max(1, round(self._duracion_horas / 24, 1))
            self._costo_total = self._servicio.calcular_costo(
                cantidad=2, 
                dias=dias, 
                tipo_equipo="proyector"
            )
        elif nombre_servicio == "Asesoria":
            self._costo_total = self._servicio.calcular_costo(
                horas=self._duracion_horas, 
                nivel="senior",
                impuesto=0.19
            )
        else:
            # Por defecto
            self._costo_total = self._servicio.calcular_costo(duracion=self._duracion_horas)
    
    # ========== MÉTODOS DE NEGOCIO ==========
    def confirmar(self):
        """Confirma la reserva y calcula el costo"""
        if self._estado != "pendiente":
            raise EstadoReservaInvalidoError(f"No se puede confirmar una reserva en estado '{self._estado}'")
        
        self._estado = "confirmada"
        self._calcular_costo()
    
    def cancelar(self):
        """Cancela la reserva"""
        if self._estado == "completada":
            raise EstadoReservaInvalidoError("No se puede cancelar una reserva ya completada")
        
        if self._estado == "cancelada":
            raise EstadoReservaInvalidoError("La reserva ya está cancelada")
        
        self._estado = "cancelada"
    
    def completar(self):
        """Marca la reserva como completada"""
        if self._estado not in ["confirmada", "pendiente"]:
            raise EstadoReservaInvalidoError(f"No se puede completar una reserva en estado '{self._estado}'")
        
        self._estado = "completada"
    
    # ========== IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS ==========
    def validar(self) -> bool:
        """Validación básica de la reserva"""
        if not self._cliente:
            return False
        if not self._servicio:
            return False
        if self._duracion_horas <= 0:
            return False
        return True
    
    def mostrar_info(self) -> str:
        """Retorna información formateada de la reserva"""
        costo_str = f"${self._costo_total:,.2f}" if self._costo_total else "No calculado"
        # ¡CORREGIDO! Ahora usa self.id_entidad en lugar de self.id
        return f"""
        ┌─────────────────────────────────────────┐
        │ RESERVA: {self.id_entidad}
        │ Cliente: {self._cliente.nombre}
        │ Servicio: {self._servicio.nombre}
        │ Fecha: {self._fecha_inicio.strftime('%Y-%m-%d %H:%M')}
        │ Duración: {self._duracion_horas} horas
        │ Estado: {self._estado.upper()}
        │ Costo: {costo_str}
        └─────────────────────────────────────────┘
        """
    
    def __str__(self):
        return f"Reserva({self.id_entidad}): {self._cliente.nombre} - {self._servicio.nombre} [{self._estado}]"