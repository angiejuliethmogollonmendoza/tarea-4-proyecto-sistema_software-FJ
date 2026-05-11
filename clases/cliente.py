"""
Clase Cliente con validaciones robustas y encapsulación
"""

from .entidad import Entidad
from .excepciones import DatosClienteInvalidosError
import re

class Cliente(Entidad):
    """
    Representa un cliente del sistema
    """
    
    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        """
        Crea un nuevo cliente
        
        Args:
            cedula: Número de identificación (único)
            nombre: Nombre completo
            email: Correo electrónico
            telefono: Número de contacto
        """
        super().__init__(cedula)
        self._cedula = cedula
        self._nombre = nombre
        self._email = email
        self._telefono = telefono
        self._activo = True
        
        # Validar al crear
        self.validar()
    
    # ========== PROPIEDADES (Getters) ==========
    @property
    def cedula(self):
        return self._cedula
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def email(self):
        return self._email
    
    @property
    def telefono(self):
        return self._telefono
    
    @property
    def activo(self):
        return self._activo
    
    # ========== SETTERS CON VALIDACIÓN ==========
    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise DatosClienteInvalidosError("El nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip()
    
    @email.setter
    def email(self, valor):
        # Validar formato de email con expresión regular
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, valor):
            raise DatosClienteInvalidosError(f"Email inválido: {valor}")
        self._email = valor.strip()
    
    @telefono.setter
    def telefono(self, valor):
        if not valor or len(valor.strip()) < 7:
            raise DatosClienteInvalidosError("El teléfono debe tener al menos 7 dígitos")
        self._telefono = valor.strip()
    
    # ========== MÉTODOS DE NEGOCIO ==========
    def desactivar(self):
        """Desactiva el cliente (no se elimina, se inactiva)"""
        self._activo = False
    
    def activar(self):
        """Reactiva un cliente desactivado"""
        self._activo = True
    
    # ========== IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS ==========
    def validar(self) -> bool:
        """
        Valida todos los datos del cliente
        Lanza excepción si algún dato es inválido
        """
        if not self._cedula or len(self._cedula.strip()) < 5:
            raise DatosClienteInvalidosError("La cédula debe tener al menos 5 caracteres")
        
        if not self._nombre or len(self._nombre.strip()) < 3:
            raise DatosClienteInvalidosError("El nombre debe tener al menos 3 caracteres")
        
        if not self._telefono or len(self._telefono.strip()) < 7:
            raise DatosClienteInvalidosError("El teléfono debe tener al menos 7 dígitos")
        
        return True
    
    def mostrar_info(self) -> str:
        """Retorna información formateada del cliente"""
        estado = "Activo" if self._activo else "Inactivo"
        return f"Cliente: {self._nombre} | Cédula: {self._cedula} | Email: {self._email} | Tel: {self._telefono} | Estado: {estado}"
    
    def __str__(self):
        return self.mostrar_info()

