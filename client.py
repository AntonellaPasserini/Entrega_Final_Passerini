"""Cliente de logging distribuido.

Se conecta al servidor de logging y envía mensajes que serán registrados.
"""

import socket
import sys
from datetime import datetime


class LogClient:
    """Cliente que envía mensajes al servidor de logging.
    
    Se conecta a un servidor de logging y permite enviar mensajes
    que serán registrados con información de origen.
    
    Attributes:
        host (str): Dirección del servidor.
        port (int): Puerto del servidor.
        socket (socket.socket): Socket de conexión con el servidor.
        connected (bool): Indica si está conectado al servidor.
    
    Example:
        >>> client = LogClient("localhost", 9999)
        >>> client.connect()
        >>> client.send_message("Mensaje de prueba")
        >>> client.disconnect()
    """
    
    def __init__(self, host: str = "localhost", port: int = 9999):
        """Inicializa el cliente de logging.
        
        Args:
            host (str): Dirección del servidor. Defecto: "localhost"
            port (int): Puerto del servidor. Defecto: 9999
        """
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """Se conecta al servidor de logging.
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario.
        
        Example:
            >>> client = LogClient()
            >>> if client.connect():
            ...     print("Conectado al servidor")
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✓ Conectado al servidor en {self.host}:{self.port}")
            return True
        
        except ConnectionRefusedError:
            print(f"✗ Error: No se pudo conectar a {self.host}:{self.port}")
            print("  Asegúrate de que el servidor está ejecutándose")
            return False
        
        except Exception as exc:
            print(f"✗ Error de conexión: {exc}")
            return False
    
    def send_message(self, message: str) -> bool:
        """Envía un mensaje al servidor.
        
        Args:
            message (str): Mensaje a enviar.
        
        Returns:
            bool: True si el mensaje se envió exitosamente.
        
        Example:
            >>> client.send_message("Error crítico en aplicación")
        """
        if not self.connected:
            print("✗ No estás conectado al servidor")
            return False
        
        try:
            # Enviar mensaje
            self.socket.sendall(message.encode('utf-8'))
            
            # Recibir respuesta del servidor
            response = self.socket.recv(1024).decode('utf-8')
            print(f"← {response.strip()}")
            
            return True
        
        except Exception as exc:
            print(f"✗ Error enviando mensaje: {exc}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Se desconecta del servidor.
        
        Example:
            >>> client.disconnect()
        """
        try:
            if self.socket:
                self.send_message("exit")
                self.socket.close()
                self.connected = False
                print("✓ Desconectado del servidor")
        
        except Exception as exc:
            print(f"✗ Error al desconectar: {exc}")
    
    def interactive_mode(self) -> None:
        """Inicia modo interactivo donde el usuario puede enviar mensajes.
        
        El usuario puede escribir mensajes que serán enviados al servidor.
        Escribe 'exit' para salir.
        
        Example:
            >>> client.connect()
            >>> client.interactive_mode()
        """
        print("\n=== Modo Interactivo ===")
        print("Escribe mensajes para enviar al servidor")
        print("(Escribe 'exit' para salir)\n")
        
        while self.connected:
            try:
                message = input(">>> ").strip()
                
                if not message:
                    continue
                
                if message.lower() == "exit":
                    self.disconnect()
                    break
                
                # Agregar timestamp al mensaje
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                full_message = f"[{timestamp}] {message}"
                
                self.send_message(full_message)
            
            except KeyboardInterrupt:
                print("\n✓ Saliendo...")
                self.disconnect()
                break
            
            except Exception as exc:
                print(f"✗ Error: {exc}")
                self.disconnect()
                break


def send_single_message(message: str) -> None:
    """Función auxiliar para enviar un único mensaje al servidor.
    
    Args:
        message (str): Mensaje a enviar.
    
    Example:
        >>> send_single_message("Error en base de datos")
    """
    client = LogClient()
    
    if client.connect():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        client.send_message(full_message)
        client.disconnect()
    else:
        sys.exit(1)


def main():
    """Función principal del cliente de logging.
    
    Permite usar el cliente en modo interactivo.
    """
    print("\n=== Cliente de Logging Distribuido ===\n")
    
    # Crear cliente
    client = LogClient()
    
    # Conectar al servidor
    if not client.connect():
        sys.exit(1)
    
    # Entrar en modo interactivo
    client.interactive_mode()


if __name__ == "__main__":
    # Si se proporciona un argumento, se envía como mensaje único
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        send_single_message(message)
    else:
        # Modo interactivo
        main()
