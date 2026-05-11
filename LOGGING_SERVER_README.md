# Sistema de Logging Distribuido

## Descripción

Sistema cliente-servidor para recopilar y registrar mensajes de múltiples clientes en un servidor centralizado. Los mensajes se registran en archivos de log con información de origen, timestamp y contenido.

## Características

- **Servidor multicliente**: Maneja múltiples clientes simultáneamente usando threads
- **Conexión TCP**: Comunicación confiable entre cliente y servidor
- **Logging centralizado**: Registra todos los mensajes en archivos estructurados
- **Timestamps**: Cada mensaje incluye información temporal
- **Información de origen**: Se registra la dirección IP y puerto del cliente
- **Sin dependencias externas**: Solo usa bibliotecas estándar de Python

## Estructura de Archivos

```
├── server.py           # Servidor de logging
├── client.py           # Cliente de logging
├── demo_logging.py     # Script de demostración
└── logs/
    ├── server.log           # Log de eventos del servidor
    └── client_messages.log  # Log de mensajes de clientes
```

## Uso

### 1. Iniciar el Servidor

```bash
python server.py
```

**Salida esperada:**
```
✓ Servidor de logging iniciado
✓ Escuchando en localhost:9999
✓ Logs guardados en: ./logs/

(Presiona Ctrl+C para detener el servidor)
```

### 2. Usar el Cliente (Modo Interactivo)

En otra terminal:

```bash
python client.py
```

**Ejemplo:**
```
=== Cliente de Logging Distribuido ===

✓ Conectado al servidor en localhost:9999

=== Modo Interactivo ===
Escribe mensajes para enviar al servidor
(Escribe 'exit' para salir)

>>> Error en la base de datos
← [Servidor] Mensaje recibido: [2026-05-11 18:14:36] Error en la base de datos

>>> Usuario autenticado
← [Servidor] Mensaje recibido: [2026-05-11 18:14:40] Usuario autenticado

>>> exit
✓ Desconectado del servidor
```

### 3. Usar el Cliente (Mensaje Único)

Para enviar un mensaje sin modo interactivo:

```bash
python client.py "Error crítico en aplicación"
```

### 4. Ejecutar Demostración

Se incluye un script de demostración que muestra:
- Clientes simple
- Múltiples clientes concurrentes
- Registro de diferentes tipos de eventos

```bash
python demo_logging.py
```

## Formatos de Log

### server.log
Eventos del servidor (conexiones, desconexiones, errores):

```
2026-05-11 18:14:35 | SERVER | INFO | Servidor iniciado en localhost:9999
2026-05-11 18:14:36 | SERVER | INFO | Cliente #1 conectado desde 127.0.0.1:54321
2026-05-11 18:14:37 | SERVER | INFO | Mensaje recibido de Cliente #1: Error en BD
2026-05-11 18:14:40 | SERVER | INFO | Cliente #1 desconectado
```

### client_messages.log
Mensajes de clientes (contenido de mensajes con origen):

```
2026-05-11 18:14:37 | CLIENT MESSAGE | [Cliente #1 | 127.0.0.1:54321] Error en BD
2026-05-11 18:14:39 | CLIENT MESSAGE | [Cliente #2 | 127.0.0.1:54322] Usuario autenticado
2026-05-11 18:14:40 | CLIENT MESSAGE | [Cliente #1 | 127.0.0.1:54321] Operación completada
```

## Configuración

### Cambiar Puerto del Servidor

En `server.py`:
```python
if __name__ == "__main__":
    server = LogServer(host="localhost", port=8888)  # Cambiar puerto
    server.start()
```

### Cambiar Servidor en Cliente

En `client.py`:
```python
client = LogClient(host="localhost", port=8888)  # Cambiar puerto
client.connect()
```

## API del Servidor

### Clase `LogServer`

```python
server = LogServer(host="localhost", port=9999)
server.start()      # Inicia el servidor
server.stop()       # Detiene el servidor
```

### Métodos internos

- `_accept_connections()`: Loop que acepta nuevas conexiones
- `_handle_client()`: Maneja comunicación con cada cliente
- `_setup_server_logger()`: Configura logging del servidor
- `_setup_client_logger()`: Configura logging de mensajes

## API del Cliente

### Clase `LogClient`

```python
client = LogClient(host="localhost", port=9999)
client.connect()                      # Conecta al servidor
client.send_message("Mi mensaje")     # Envía un mensaje
client.interactive_mode()             # Modo interactivo
client.disconnect()                   # Desconecta
```

### Funciones auxiliares

```python
send_single_message("Mensaje")  # Envía un mensaje y desconecta
```

## Ejemplo de Uso Programático

```python
from client import LogClient

# Crear cliente
client = LogClient()

# Conectar
if client.connect():
    # Enviar mensajes
    client.send_message("Aplicación iniciada")
    client.send_message("Operación completada")
    
    # Desconectar
    client.disconnect()
```

## Manejo de Errores

El sistema maneja los siguientes casos:

- **Servidor no disponible**: El cliente reporta error de conexión
- **Cliente desconectado abruptamente**: El servidor registra la desconexión
- **Mensajes vacíos**: Se ignoran
- **Comando 'exit'**: Desconexión limpia

## Características de Logging

- ✓ Timestamps automáticos
- ✓ Identificación de cliente
- ✓ Separación de logs (servidor vs clientes)
- ✓ Salida a consola y archivo
- ✓ Información de IP y puerto
- ✓ Manejo de excepciones

## Limitaciones

- Puerto fijo (configurable)
- Máximo 5 conexiones en cola de escucha
- Tamaño máximo de mensaje: 1024 bytes
- Almacenamiento en memoria del contador de clientes

## Mejoras Futuras

- [ ] Autenticación de clientes
- [ ] Cifrado de comunicaciones (SSL/TLS)
- [ ] Rotación de archivos de log
- [ ] Base de datos para almacenar logs
- [ ] Dashboard web para ver logs en tiempo real
- [ ] Diferentes niveles de log (DEBUG, INFO, WARNING, ERROR)
- [ ] Filtrado de mensajes
- [ ] Compresión de logs antiguos

## Notas de Seguridad

Este es un sistema de demostración. Para uso en producción, considera:

1. Implementar SSL/TLS para conexiones seguras
2. Agregar autenticación de clientes
3. Validar y sanitizar mensajes
4. Implementar límites de tasa (rate limiting)
5. Usar bases de datos para almacenamiento persistente

## Licencia

Código educativo de demostración.
