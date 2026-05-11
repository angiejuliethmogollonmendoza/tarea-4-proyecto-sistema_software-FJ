"""
SISTEMA SOFT FJ - DEMOSTRACIÓN COMPLETA
"""

from datetime import datetime, timedelta
from clases.gestor import GestorSoftFJ
from clases.excepciones import *

def main():
    print("="*60)
    print("SISTEMA DE GESTIÓN SOFT FJ")
    print("="*60)
    
    sistema = GestorSoftFJ()
    
    # OPERACIÓN 1: Cliente válido
    print("\n1. Registrar cliente válido:")
    try:
        c1 = sistema.registrar_cliente("12345678", "Ana López", "ana@email.com", "3001234567")
        print(f"   ✓ {c1.mostrar_info()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # OPERACIÓN 2: Otro cliente válido
    print("\n2. Registrar otro cliente:")
    try:
        c2 = sistema.registrar_cliente("87654321", "Carlos Ruiz", "carlos@email.com", "3109876543")
        print(f"   ✓ {c2.mostrar_info()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # OPERACIÓN 3: Cliente con datos inválidos (MANEJO DE EXCEPCIÓN)
    print("\n3. Intentar cliente inválido (nombre corto):")
    try:
        c3 = sistema.registrar_cliente("111111", "A", "a@b.com", "1234567")
        print(f"   ✓ Esto no debería aparecer")
    except DatosClienteInvalidosError as e:
        print(f"   ✓ EXCEPCIÓN CAPTURADA: {e}")
    
    # OPERACIÓN 4: Cliente duplicado (MANEJO DE EXCEPCIÓN)
    print("\n4. Intentar cliente duplicado:")
    try:
        c4 = sistema.registrar_cliente("12345678", "Otra", "otra@email.com", "3111111111")
        print(f"   ✓ Esto no debería aparecer")
    except ClienteYaExisteError as e:
        print(f"   ✓ EXCEPCIÓN CAPTURADA: {e}")
    
    # OPERACIÓN 5: Reserva exitosa
    print("\n5. Crear reserva exitosa (Sala):")
    try:
        fecha = datetime.now() + timedelta(days=3)
        r1 = sistema.crear_reserva("R001", "12345678", "SAL001", fecha, 4)
        print(f"   ✓ Reserva creada - Costo: ${r1.costo_total:,.2f}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # OPERACIÓN 6: Reserva con cliente inexistente (MANEJO DE EXCEPCIÓN)
    print("\n6. Reserva con cliente inexistente:")
    try:
        fecha = datetime.now() + timedelta(days=2)
        r2 = sistema.crear_reserva("R002", "99999999", "SAL001", fecha, 3)
        print(f"   ✓ Esto no debería aparecer")
    except ClienteNoEncontradoError as e:
        print(f"   ✓ EXCEPCIÓN CAPTURADA: {e}")
    
    # OPERACIÓN 7: Reserva con fecha pasada (MANEJO DE EXCEPCIÓN)
    print("\n7. Reserva con fecha pasada:")
    try:
        fecha = datetime.now() - timedelta(days=1)
        r3 = sistema.crear_reserva("R003", "12345678", "SAL001", fecha, 2)
        print(f"   ✓ Esto no debería aparecer")
    except FechaInvalidaError as e:
        print(f"   ✓ EXCEPCIÓN CAPTURADA: {e}")
    
    # OPERACIÓN 8: Cancelar reserva
    print("\n8. Cancelar reserva existente:")
    try:
        r_cancelada = sistema.cancelar_reserva("R001")
        print(f"   ✓ Reserva cancelada. Estado: {r_cancelada.estado}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # OPERACIÓN 9: Listar reservas
    print("\n9. Listar todas las reservas:")
    for r in sistema.listar_reservas():
        print(r.mostrar_info())
    
    # OPERACIÓN 10: Mostrar cálculos polimórficos
    print("\n10. Cálculos polimórficos de servicios:")
    for s in sistema.listar_servicios():
        try:
            if type(s).__name__ == "ReservaSala":
                costo = s.calcular_costo(horas=3, tipo_sala="ejecutiva")
                print(f"   {s.nombre}: 3h sala ejecutiva = ${costo:,.2f}")
            elif type(s).__name__ == "AlquilerEquipo":
                costo = s.calcular_costo(cantidad=2, dias=5, tipo_equipo="proyector")
                print(f"   {s.nombre}: 2 proyectores 5 días = ${costo:,.2f}")
            elif type(s).__name__ == "Asesoria":
                costo = s.calcular_costo(horas=4, nivel="senior")
                print(f"   {s.nombre}: 4h senior = ${costo:,.2f}")
        except Exception as e:
            print(f"   Error: {e}")
    
    # OPERACIÓN 11 y 12: Estadísticas + muestra de logs
    print("\n11. Estadísticas del sistema:")
    sistema.mostrar_estadisticas()
    
    print("\n12. Verificar logs (se crearon en logs/sistema.log)")
    print("\n" + "="*60)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("📁 Revisa el archivo logs/sistema.log para ver los errores registrados")
    print("="*60)

if __name__ == "__main__":
    main()