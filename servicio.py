"""
Clase abstracta Servicio - Define la estructura de todos los servicios
"""

from abc import ABC, abstractmethod
from .entidad import Entidad
from .excepciones import ParametrosServicioInvalidosError

class Servicio(Entidad, ABC):
    """
    Clase abstracta que define la estructura de todos los servicios
    """
    
    def __init__(self, codigo: str, nombre: str, precio_base: float):
        super().__init__(codigo)
        self._codigo = codigo
        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = True
    
    # ========== PROPIEDADES ==========
    @property
    def codigo(self):
        return self._codigo
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def precio_base(self):
        return self._precio_base
    
    @property
    def disponible(self):
        return self._disponible
    
    # ========== MÉTODOS ==========
    def set_disponible(self, estado: bool):
        """Cambia la disponibilidad del servicio"""
        self._disponible = estado
    
    # ========== MÉTODOS ABSTRACTOS (Polimórficos) ==========
    @abstractmethod
    def calcular_costo(self, **kwargs) -> float:
        """
        Calcula el costo del servicio.
        Cada servicio implementa su propia fórmula.
        
        Args:
            **kwargs: Parámetros variables según el tipo de servicio
        Returns:
            float: Costo total
        """
        pass
    
    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción del servicio"""
        pass
    
    # ========== IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS ==========
    def validar(self) -> bool:
        """Valida los datos básicos del servicio"""
        if not self._codigo or len(self._codigo) < 3:
            raise ParametrosServicioInvalidosError("El código debe tener al menos 3 caracteres")
        if not self._nombre or len(self._nombre) < 3:
            raise ParametrosServicioInvalidosError("El nombre debe tener al menos 3 caracteres")
        if self._precio_base <= 0:
            raise ParametrosServicioInvalidosError("El precio base debe ser mayor a 0")
        return True
    
    def mostrar_info(self) -> str:
        """Información básica del servicio"""
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio: {self._nombre} | Código: {self._codigo} | Precio base: ${self._precio_base:,.2f} | {estado}"
