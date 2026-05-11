"""Script de demostración del sistema de logging distribuido.

Muestra cómo usar el servidor y cliente de logging para registrar
mensajes desde múltiples clientes.
"""

import time
import subprocess
import sys
from client import LogClient


def demo_single_client():
    """Demuestra el envío de un único mensaje desde un cliente."""
    print("\n" + "="*60)
    print("DEMO 1: Cliente Simple - Envío de Mensajes Únicos")
    print("="*60)
    
    messages = [
        "Aplicación iniciada correctamente",
        "Usuario autenticado: admin",
        "Operación de base de datos completada",
        "Advertencia: Recursos limitados",
        "Error: Conexión perdida"
    ]
    
    client = LogClient()
    
    if not client.connect():
        print("No se pudo conectar al servidor")
        return
    
    print("\nEnviando mensajes de prueba...\n")
    
    for message in messages:
        print(f"Enviando: {message}")
        client.send_message(message)
        time.sleep(0.5)
    
    client.disconnect()


def demo_multiple_clients():
    """Demuestra múltiples clientes enviando mensajes simultáneamente."""
    print("\n" + "="*60)
    print("DEMO 2: Múltiples Clientes - Mensajes Concurrentes")
    print("="*60)
    
    messages_per_client = {
        "Cliente A": [
            "Iniciando proceso A",
            "Procesando datos A",
            "Completado proceso A"
        ],
        "Cliente B": [
            "Iniciando proceso B",
            "Procesando datos B",
            "Completado proceso B"
        ],
        "Cliente C": [
            "Iniciando proceso C",
            "Procesando datos C",
            "Completado proceso C"
        ]
    }
    
    print("\nEnviando mensajes desde múltiples clientes...\n")
    
    for client_name, messages in messages_per_client.items():
        client = LogClient()
        
        if not client.connect():
            print(f"No se pudo conectar desde {client_name}")
            continue
        
        for message in messages:
            full_msg = f"{client_name}: {message}"
            print(f"[{client_name}] Enviando: {message}")
            client.send_message(full_msg)
            time.sleep(0.3)
        
        client.disconnect()


def demo_error_handling():
    """Demuestra el manejo de errores."""
    print("\n" + "="*60)
    print("DEMO 3: Regitro de Errores")
    print("="*60)
    
    error_messages = [
        "ERROR: Archivo no encontrado",
        "ERROR: Permisos insuficientes",
        "ERROR: Timeout en conexión",
        "WARNING: Memoria casi llena",
        "INFO: Conexión establecida",
        "SUCCESS: Operación completada"
    ]
    
    client = LogClient()
    
    if not client.connect():
        print("No se pudo conectar al servidor")
        return
    
    print("\nRegistrando diferentes tipos de eventos...\n")
    
    for message in error_messages:
        print(f"Enviando: {message}")
        client.send_message(message)
        time.sleep(0.4)
    
    client.disconnect()


def main():
    """Ejecuta las demostraciones."""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN DEL SISTEMA DE LOGGING DISTRIBUIDO")
    print("="*60)
    
    print("\n⚠️  Asegúrate de que el servidor está ejecutándose:")
    print("   python server.py")
    input("\nPresiona Enter para continuar...")
    
    try:
        # Ejecutar demos
        demo_single_client()
        time.sleep(1)
        
        demo_multiple_clients()
        time.sleep(1)
        
        demo_error_handling()
        
        print("\n" + "="*60)
        print("DEMOSTRACIONES COMPLETADAS")
        print("="*60)
        print("\n✓ Revisa los archivos de log en la carpeta 'logs/'")
        print("  - logs/server.log (eventos del servidor)")
        print("  - logs/client_messages.log (mensajes de clientes)\n")
    
    except KeyboardInterrupt:
        print("\n\nDeomstración cancelada por el usuario")
    
    except Exception as exc:
        print(f"\n✗ Error durante la demostración: {exc}")


if __name__ == "__main__":
    main()
