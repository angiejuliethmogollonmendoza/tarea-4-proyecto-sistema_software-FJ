"""
Controla todas las operaciones: clientes, servicios y reservas
"""

import logging
import os
from datetime import datetime
from .excepciones import *
from .cliente import Cliente
from .servicios_concretos import ReservaSala, AlquilerEquipo, Asesoria
from .reserva import Reserva

class GestorSoftFJ:

    
    def __init__(self):
        # Crear directorio de logs si no existe
        os.makedirs("logs", exist_ok=True)
        
        # Configurar el sistema de logging
        logging.basicConfig(
            filename="logs/sistema.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
        # Almacenamiento en memoria (sin base de datos)
        self.clientes = []
        self.servicios = []
        self.reservas = []
        
        # Inicializar servicios disponibles
        self._inicializar_servicios()
        
        self.logger.info("=== SISTEMA SOFT FJ INICIADO ===")
    
    def _inicializar_servicios(self):
        """Crea los servicios base del sistema"""
        self.servicios = [
            ReservaSala(),
            AlquilerEquipo(),
            Asesoria()
        ]
        self.logger.info("Servicios inicializados: 3 servicios disponibles")
    
    # ========== OPERACIONES CON CLIENTES ==========
    
    def registrar_cliente(self, cedula: str, nombre: str, email: str, telefono: str) -> Cliente:
        """
        Registra un nuevo cliente en el sistema
        
        Returns:
            Cliente: El cliente creado
            
        Raises:
            ClienteYaExisteError: Si ya existe un cliente con esa cédula
            DatosClienteInvalidosError: Si los datos son inválidos
        """
        try:
            # Verificar si ya existe un cliente con esa cédula
            for cliente in self.clientes:
                if cliente.cedula == cedula:
                    raise ClienteYaExisteError(f"Ya existe un cliente con cédula {cedula}")
            
            # Crear nuevo cliente (la validación ocurre dentro del constructor)
            nuevo_cliente = Cliente(cedula, nombre, email, telefono)
            self.clientes.append(nuevo_cliente)
            
            self.logger.info(f"✓ Cliente registrado: {cedula} - {nombre}")
            return nuevo_cliente
            
        except (ClienteYaExisteError, DatosClienteInvalidosError) as e:
            self.logger.error(f"✗ Error al registrar cliente {cedula}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"✗ Error inesperado al registrar cliente: {str(e)}")
            raise
    
    def buscar_cliente(self, cedula: str) -> Cliente:
        """
        Busca un cliente por su cédula
        
        Raises:
            ClienteNoEncontradoError: Si no existe el cliente
        """
        for cliente in self.clientes:
            if cliente.cedula == cedula:
                return cliente
        raise ClienteNoEncontradoError(f"No se encontró cliente con cédula {cedula}")
    
    def listar_clientes(self) -> list:
        """Retorna la lista de todos los clientes"""
        return self.clientes.copy()
    
    # ========== OPERACIONES CON SERVICIOS ==========
    
    def listar_servicios(self) -> list:
        """Retorna todos los servicios disponibles"""
        return self.servicios.copy()
    
    def buscar_servicio(self, codigo: str):
        """
        Busca un servicio por su código
        
        Raises:
            ServicioNoEncontradoError: Si no existe el servicio
        """
        for servicio in self.servicios:
            if servicio.codigo == codigo:
                return servicio
        raise ServicioNoEncontradoError(f"Servicio {codigo} no encontrado")
    
    # ========== OPERACIONES CON RESERVAS ==========
    
    def crear_reserva(self, id_reserva: str, cedula_cliente: str, codigo_servicio: str, 
                      fecha_inicio: datetime, duracion_horas: float) -> Reserva:
        """
        Crea una nueva reserva con manejo robusto de excepciones
        
        Returns:
            Reserva: La reserva creada
            
        Raises:
            ClienteNoEncontradoError: Si el cliente no existe
            ServicioNoEncontradoError: Si el servicio no existe
            ServicioNoDisponibleError: Si el servicio no está disponible
            FechaInvalidaError: Si la fecha es pasada
        """
        try:
            
            cliente = self.buscar_cliente(cedula_cliente)
            
            
            servicio = self.buscar_servicio(codigo_servicio)
            
           
            if not servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio {servicio.nombre} no está disponible")
            
            
            for reserva in self.reservas:
                if reserva.id_entidad == id_reserva:
                    raise ReservaException(f"Ya existe una reserva con ID {id_reserva}")
            
           
            nueva_reserva = Reserva(id_reserva, cliente, servicio, fecha_inicio, duracion_horas)
            
           
            nueva_reserva.confirmar()
            
           
            self.reservas.append(nueva_reserva)
            
            self.logger.info(f"✓ Reserva creada: {id_reserva} - Cliente: {cedula_cliente} - Servicio: {codigo_servicio}")
            return nueva_reserva
            
        except (ClienteNoEncontradoError, ServicioNoEncontradoError, 
                ServicioNoDisponibleError, FechaInvalidaError, ReservaException) as e:
            self.logger.error(f"✗ Error al crear reserva {id_reserva}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"✗ Error inesperado en reserva {id_reserva}: {str(e)}")
            raise
    
    def cancelar_reserva(self, id_reserva: str) -> Reserva:
        """Cancela una reserva existente"""
        try:
            for reserva in self.reservas:
                if reserva.id_entidad == id_reserva:
                    reserva.cancelar()
                    self.logger.info(f"✓ Reserva cancelada: {id_reserva}")
                    return reserva
            raise ReservaException(f"No se encontró reserva con ID {id_reserva}")
        except Exception as e:
            self.logger.error(f"✗ Error al cancelar reserva {id_reserva}: {str(e)}")
            raise
    
    def listar_reservas(self) -> list:
        """Retorna todas las reservas"""
        return self.reservas.copy()
    
    # ========== ESTADÍSTICAS ==========
    
    def mostrar_estadisticas(self):
        """Muestra un resumen del sistema"""
        print("\n" + "="*50)
        print(" ESTADÍSTICAS DEL SISTEMA SOFT FJ")
        print("="*50)
        print(f"  Clientes registrados: {len(self.clientes)}")
        print(f"  Servicios disponibles: {len(self.servicios)}")
        print(f"  Reservas realizadas: {len(self.reservas)}")
        
        reservas_activas = [r for r in self.reservas if r.estado in ["pendiente", "confirmada"]]
        print(f"  Reservas activas: {len(reservas_activas)}")
        
        print("\n CLIENTES:")
        for c in self.clientes:
            print(f"    • {c.nombre} ({c.cedula})")
        
        print("\nSERVICIOS:")
        for s in self.servicios:
            estado = "✓ Disponible" if s.disponible else "✗ No disponible"
            print(f"    • {s.nombre} - ${s.precio_base:,.0f} - {estado}")
        
        print("="*50)