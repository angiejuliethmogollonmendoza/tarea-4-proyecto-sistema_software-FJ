"""
Clase abstracta base - Todas las entidades heredan de aquí
"""

from abc import ABC, abstractmethod
from datetime import datetime

class Entidad(ABC):
    """
    Clase abstracta que define el comportamiento común de todas las entidades
    """
    
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad
        self._fecha_creacion = datetime.now()
    
    @property
    def id_entidad(self):
        """Retorna el identificador único"""
        return self._id_entidad
    
    @property
    def fecha_creacion(self):
        """Retorna la fecha de creación"""
        return self._fecha_creacion
    
    @abstractmethod
    def validar(self) -> bool:
        """
        Valida que la entidad tenga datos correctos.
        Cada clase hija debe implementar este método.
        """
        pass
    
    @abstractmethod
    def mostrar_info(self) -> str:
        """
        Retorna información formateada de la entidad.
        Cada clase hija debe implementar este método.
        """
        pass
    
    def __str__(self):
        return f"Entidad({self._id_entidad})"