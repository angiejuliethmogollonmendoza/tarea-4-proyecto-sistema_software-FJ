"""
Implementaciones concretas de los servicios
Contiene: ReservaSala, AlquilerEquipo, Asesoria
"""

from .servicio import Servicio
from .excepciones import ParametrosServicioInvalidosError, ServicioNoDisponibleError

# ========== SERVICIO 1: RESERVA DE SALAS ==========
class ReservaSala(Servicio):
    """
    Servicio de reserva de salas
    Costo = precio_base * horas * factor_tipo_sala
    """
    
    FACTORES_SALA = {
        "basica": 1.0,
        "ejecutiva": 1.5,
        "presidencial": 2.5
    }
    
    def __init__(self):
        super().__init__("SAL001", "Reserva de Salas", 50000)
        self._capacidad_maxima = 50
    
    def validar_parametros(self, **kwargs):
        """Valida horas y tipo de sala"""
        if "horas" not in kwargs:
            raise ParametrosServicioInvalidosError("Falta el parámetro 'horas'")
        
        horas = kwargs.get("horas")
        if horas <= 0 or horas > 24:
            raise ParametrosServicioInvalidosError("Las horas deben ser entre 1 y 24")
        
        tipo_sala = kwargs.get("tipo_sala", "basica")
        if tipo_sala not in self.FACTORES_SALA:
            raise ParametrosServicioInvalidosError(f"Tipo de sala inválido. Opciones: {list(self.FACTORES_SALA.keys())}")
        
        return True
    
    def calcular_costo(self, **kwargs):
        """Calcula costo de reserva de sala"""
        if not self.disponible:
            raise ServicioNoDisponibleError("El servicio de reserva de salas no está disponible")
        
        self.validar_parametros(**kwargs)
        horas = kwargs.get("horas", 0)
        tipo_sala = kwargs.get("tipo_sala", "basica")
        
        costo = self.precio_base * horas * self.FACTORES_SALA[tipo_sala]
        return round(costo, 2)
    
    def describir(self):
        return f"Reserva de salas empresariales. Capacidad máxima: {self._capacidad_maxima} personas"
    
    def mostrar_info(self):
        base = super().mostrar_info()
        return base + f" | Capacidad: {self._capacidad_maxima}"


# ========== SERVICIO 2: ALQUILER DE EQUIPOS ==========
class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos
    Costo = precio_base * cantidad * dias
    """
    
    EQUIPOS_DISPONIBLES = ["proyector", "computador", "pantalla", "sonido", "videoconferencia"]
    
    def __init__(self):
        super().__init__("EQP001", "Alquiler de Equipos", 25000)
    
    def validar_parametros(self, **kwargs):
        """Valida cantidad, días y tipo de equipo"""
        if "cantidad" not in kwargs:
            raise ParametrosServicioInvalidosError("Falta el parámetro 'cantidad'")
        if "dias" not in kwargs:
            raise ParametrosServicioInvalidosError("Falta el parámetro 'dias'")
        if "tipo_equipo" not in kwargs:
            raise ParametrosServicioInvalidosError("Falta el parámetro 'tipo_equipo'")
        
        cantidad = kwargs.get("cantidad")
        if cantidad <= 0 or cantidad > 10:
            raise ParametrosServicioInvalidosError("La cantidad debe ser entre 1 y 10")
        
        dias = kwargs.get("dias")
        if dias <= 0:
            raise ParametrosServicioInvalidosError("Los días deben ser un número positivo")
        
        tipo_equipo = kwargs.get("tipo_equipo")
        if tipo_equipo not in self.EQUIPOS_DISPONIBLES:
            raise ParametrosServicioInvalidosError(f"Equipo no disponible. Opciones: {self.EQUIPOS_DISPONIBLES}")
        
        return True
    
    def calcular_costo(self, **kwargs):
        """Calcula costo de alquiler de equipos"""
        if not self.disponible:
            raise ServicioNoDisponibleError("El servicio de alquiler de equipos no está disponible")
        
        self.validar_parametros(**kwargs)
        cantidad = kwargs.get("cantidad", 0)
        dias = kwargs.get("dias", 0)
        
        costo = self.precio_base * cantidad * dias
        return round(costo, 2)
    
    def describir(self):
        return f"Alquiler de equipos tecnológicos. Equipos: {', '.join(self.EQUIPOS_DISPONIBLES)}"
    
    def mostrar_info(self):
        base = super().mostrar_info()
        return base + f" | Equipos: {', '.join(self.EQUIPOS_DISPONIBLES)}"


# ========== SERVICIO 3: ASESORÍAS ==========
class Asesoria(Servicio):
    """
    Servicio de asesorías especializadas
    Costo = precio_base * horas * factor_nivel
    """
    
    NIVELES = {
        "junior": 1.0,
        "senior": 1.8,
        "experto": 2.5
    }
    
    def __init__(self):
        super().__init__("ASE001", "Asesorías Especializadas", 80000)
    
    def validar_parametros(self, **kwargs):
        """Valida horas y nivel del asesor"""
        if "horas" not in kwargs:
            raise ParametrosServicioInvalidosError("Falta el parámetro 'horas'")
        if "nivel" not in kwargs:
            raise ParametrosServicioInvalidosError("Falta el parámetro 'nivel'")
        
        horas = kwargs.get("horas")
        if horas <= 0 or horas > 8:
            raise ParametrosServicioInvalidosError("Las horas deben ser entre 1 y 8")
        
        nivel = kwargs.get("nivel")
        if nivel not in self.NIVELES:
            raise ParametrosServicioInvalidosError(f"Nivel inválido. Opciones: {list(self.NIVELES.keys())}")
        
        return True
    
    def calcular_costo(self, **kwargs):
        """Calcula costo de asesoría (con sobrecarga de método simulada)"""
        if not self.disponible:
            raise ServicioNoDisponibleError("El servicio de asesorías no está disponible")
        
        self.validar_parametros(**kwargs)
        horas = kwargs.get("horas", 0)
        nivel = kwargs.get("nivel", "junior")
        
        # Costo base con factor por nivel
        subtotal = self.precio_base * horas * self.NIVELES[nivel]
        
        # SOBRECARGA DE MÉTODO: diferentes cálculos según parámetros opcionales
        return self._calcular_con_impuestos_y_descuento(subtotal, **kwargs)
    
    def _calcular_con_impuestos_y_descuento(self, subtotal: float, **kwargs) -> float:
        """
        SOBRECARGA: calcula costo con impuestos y descuentos (método sobrecargado implícito)
        """
        impuesto = kwargs.get("impuesto", 0.19)  # 19% IVA por defecto
        descuento = kwargs.get("descuento", 0.0)
        
        # Descuento especial para clientes frecuentes
        if kwargs.get("cliente_frecuente", False):
            descuento = max(descuento, 0.10)
        
        total = subtotal * (1 + impuesto) * (1 - descuento)
        return round(total, 2)
    
    def describir(self):
        return "Asesorías especializadas en tecnología y desarrollo de software"
    
    def mostrar_info(self):
        base = super().mostrar_info()
        return base + f" | Niveles: junior, senior, experto"
