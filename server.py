"""Servidor de logging distribuido.

Escucha conexiones de clientes, recibe mensajes y los registra en archivos de log
con timestamps y información de conexión.
"""

import socket
import threading
import logging
import os
from datetime import datetime
from pathlib import Path


class LogServer:
    """Servidor que recibe mensajes de clientes y los registra.
    
    Crea un servidor TCP que escucha en localhost:9999 (por defecto).
    Cada cliente puede enviar mensajes que son registrados con información
    de origen, timestamp y contenido.
    
    Attributes:
        host (str): Dirección del servidor (localhost por defecto).
        port (int): Puerto del servidor (9999 por defecto).
        server_socket (socket.socket): Socket del servidor.
        logger (logging.Logger): Logger para events del servidor.
        client_logger (logging.Logger): Logger para mensajes de clientes.
        running (bool): Indica si el servidor está activo.
    
    Example:
        >>> server = LogServer()
        >>> server.start()
    """
    
    def __init__(self, host: str = "localhost", port: int = 9999):
        """Inicializa el servidor de logging.
        
        Args:
            host (str): Dirección del servidor. Defecto: "localhost"
            port (int): Puerto del servidor. Defecto: 9999
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.client_count = 0
        
        # Crear directorio de logs si no existe
        self.log_dir = Path(__file__).parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar logger del servidor
        self.logger = self._setup_server_logger()
        
        # Configurar logger de clientes
        self.client_logger = self._setup_client_logger()
    
    def _setup_server_logger(self) -> logging.Logger:
        """Configura el logger para eventos del servidor.
        
        Returns:
            logging.Logger: Logger configurado para el servidor.
        """
        logger = logging.getLogger("LogServer")
        logger.setLevel(logging.INFO)
        
        # File handler
        log_file = self.log_dir / "server.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | SERVER | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Agregar handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _setup_client_logger(self) -> logging.Logger:
        """Configura el logger para mensajes de clientes.
        
        Returns:
            logging.Logger: Logger configurado para mensajes de clientes.
        """
        logger = logging.getLogger("ClientMessages")
        logger.setLevel(logging.INFO)
        
        # File handler
        log_file = self.log_dir / "client_messages.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Formatter con más detalles
        formatter = logging.Formatter(
            '%(asctime)s | CLIENT MESSAGE | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
        return logger
    
    def start(self) -> None:
        """Inicia el servidor y comienza a escuchar conexiones.
        
        Crea el socket del servidor, lo vincula al puerto especificado
        y comienza a aceptar conexiones de clientes en un thread separado.
        
        Example:
            >>> server = LogServer()
            >>> server.start()
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            self.logger.info(f"Servidor iniciado en {self.host}:{self.port}")
            
            # Iniciar thread de aceptación de conexiones
            server_thread = threading.Thread(target=self._accept_connections, daemon=True)
            server_thread.start()
            
        except Exception as exc:
            self.logger.error(f"Error al iniciar servidor: {exc}")
            raise
    
    def _accept_connections(self) -> None:
        """Acepta conexiones de clientes en un loop continuo.
        
        Espera nuevas conexiones y crea un thread separado para cada cliente.
        """
        self.logger.info("Esperando conexiones de clientes...")
        
        if self.server_socket is None:
            self.logger.error("Server socket is not initialized")
            return
        
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.client_count += 1
                client_id = self.client_count
                
                self.logger.info(f"Cliente #{client_id} conectado desde {client_address}")
                
                # Crear thread para manejar al cliente
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address, client_id),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as exc:
                if self.running:
                    self.logger.error(f"Error aceptando conexión: {exc}")
    
    def _handle_client(self, client_socket: socket.socket, 
                      client_address: tuple, client_id: int) -> None:
        """Maneja la comunicación con un cliente específico.
        
        Recibe mensajes del cliente, los procesa y registra en el log.
        
        Args:
            client_socket (socket.socket): Socket de conexión con el cliente.
            client_address (tuple): Dirección del cliente (host, puerto).
            client_id (int): ID único del cliente.
        """
        try:
            while self.running:
                # Recibir datos del cliente
                data = client_socket.recv(1024)
                
                if not data:
                    break
                
                # Decodificar mensaje
                message = data.decode('utf-8').strip()
                
                if message.lower() == "exit":
                    self.logger.info(f"Cliente #{client_id} solicitó desconexión")
                    break
                
                # Registrar mensaje del cliente
                log_entry = (
                    f"[Cliente #{client_id} | {client_address[0]}:{client_address[1]}] "
                    f"{message}"
                )
                self.client_logger.info(log_entry)
                self.logger.info(f"Mensaje recibido de Cliente #{client_id}: {message}")
                
                # Enviar confirmación al cliente
                response = f"[Servidor] Mensaje recibido: {message}\n".encode('utf-8')
                client_socket.sendall(response)
        
        except Exception as exc:
            self.logger.error(f"Error con Cliente #{client_id}: {exc}")
        
        finally:
            try:
                client_socket.close()
                self.logger.info(f"Cliente #{client_id} desconectado")
            except Exception:
                pass
    
    def stop(self) -> None:
        """Detiene el servidor y cierra todas las conexiones.
        
        Example:
            >>> server = LogServer()
            >>> server.start()
            >>> # ... hacer cosas ...
            >>> server.stop()
        """
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
                self.logger.info("Servidor detenido")
            except Exception as exc:
                self.logger.error(f"Error al detener servidor: {exc}")


def main():
    """Función principal que inicia el servidor de logging.
    
    El servidor se ejecutará continuamente hasta que se presione Ctrl+C.
    """
    server = LogServer()
    
    try:
        server.start()
        print("\n✓ Servidor de logging iniciado")
        print(f"✓ Escuchando en {server.host}:{server.port}")
        print("✓ Logs guardados en: ./logs/")
        print("\n(Presiona Ctrl+C para detener el servidor)\n")
        
        # Mantener el servidor en funcionamiento
        while True:
            threading.Event().wait(1)
    
    except KeyboardInterrupt:
        print("\n\n✓ Deteniendo servidor...")
        server.stop()
        print("✓ Servidor detenido correctamente\n")


if __name__ == "__main__":
    main()
