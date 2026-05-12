# Instrucciones breves de uso

## Descripción General

Aplicación profesional de gestión de tareas y empleados con dos componentes principales:

1. **Task DB Application**: Interfaz gráfica (GUI) basada en Tkinter para gestión de empleados y tareas
2. **Sistema de Logging Distribuido**: Servidor cliente-servidor para recopilar y registrar mensajes centralizadamente

La aplicación implementa arquitectura MVC con patrones de diseño profesionales (Facade, Factory, Decorator).

## Requisitos

- Python 3.14+
- Librerías estándar: sqlite3, tkinter (incluidas en la instalación de Python)

## Arquitectura de la Aplicación

La aplicación fue refactorizada utilizando **Programación Orientada a Objetos (POO)** y el patrón **MVC (Modelo-Vista-Controlador)** con una estructura modular profesional.

### Estructura de Carpetas

```
Entrega_Final_Passerini/
├── models/                    # Carpeta de modelos
│   ├── __init__.py
│   ├── exceptions.py          # Clases de excepciones personalizadas
│   ├── database.py            # Gestión de conexión SQLite
│   ├── employee_model.py      # Modelo para entidad Employee
│   ├── task_model.py          # Modelo para entidad Task
│   ├── backlog_model.py       # Modelo para entidad Backlog
│   └── database_manager.py    # Orquestador centralizado de BD
├── controller/                # Carpeta de controladores
│   ├── __init__.py
│   ├── app_controller.py      # Controlador centralizado
│   ├── employee_controller.py # Controlador de empleados
│   ├── task_controller.py     # Controlador de tareas
│   ├── compat.py              # Controlador TaskControllerCompat (compatibilidad)
│   └── exceptions.py          # Excepciones del controlador
├── views/                     # Carpeta de vistas
│   ├── __init__.py
│   ├── launcher.py            # Ventana principal (Launcher)
│   ├── ui_manager.py          # Gestor centralizado de UI
│   ├── base_form.py           # Clase base para formularios
│   ├── employee_form.py       # Formulario de empleados
│   ├── task_form.py           # Formulario de tareas
│   ├── lookup_form.py         # Formulario de búsqueda
│   ├── delete_employee_form.py# Formulario de eliminación
│   └── exceptions.py          # Excepciones de UI
├── validators/                # Carpeta de validadores
│   ├── __init__.py
│   ├── nonempty.py            # Validación de campos no vacíos
│   ├── email.py               # Validación de formato email
│   ├── integer.py             # Validación de números enteros
│   └── exceptions.py          # Excepciones de validación
├── utils/                     # Carpeta de utilidades
│   ├── __init__.py
│   ├── logging.py             # Funciones de logging y debugging
│   ├── formatters.py          # Funciones de formato de datos
│   ├── helpers.py             # Funciones auxiliares generales
│   └── decorators.py          # Decoradores reutilizables
├── logs/                      # Carpeta de logs (generada automáticamente)
│   ├── server.log             # Log de eventos del servidor
│   └── client_messages.log    # Log de mensajes de clientes
├── task_db_app.py             # Punto de entrada de la aplicación principal
├── server.py                  # Servidor de logging distribuido
├── client.py                  # Cliente de logging
├── demo_logging.py            # Script de demostración del logging
├── tasks.db                   # Base de datos SQLite (generada automáticamente)
└── Readme.md                  # Este archivo
```

### Componentes Principales

#### 1. **Carpeta `models/`** – Capa de Datos
Implementa una arquitectura modular separada por entidades y funcionalidades:

- **`exceptions.py`**: Clases personalizadas para manejo de errores
  - `DatabaseError`: Errores de conexión y operaciones SQL
  - `ValidationError`: Errores de validación de datos

- **`database.py`**: Clase `DatabaseConnection` que encapsula:
  - Conexión a SQLite
  - Métodos para ejecutar queries (execute, execute_one, execute_insert, execute_update)
  - Manejo centralizado de excepciones

- **`employee_model.py`**: Clase `EmployeeModel` con operaciones CRUD
  - `add_employee()`, `get_by_id()`, `get_all()`, `delete()`, `exists()`, `get_by_email()`

- **`task_model.py`**: Clase `TaskModel` con operaciones CRUD
  - `add_task()`, `get_by_id()`, `get_all()`, `get_by_employee()`, `delete()`, `count_by_employee()`

- **`backlog_model.py`**: Clase `BacklogModel` para gestión de prioridades
  - `add_to_backlog()`, `get_by_id()`, `update_priority()`, `get_high_priority()`

- **`database_manager.py`**: Clase `DatabaseManager` (patrón Facade)
  - Orquesta creación de tablas, inicialización de datos, vistas SQL
  - Proporciona acceso unificado a todos los modelos
  - Método `get_combined_data()` para datos sincronizados

#### 2. **Carpeta `controller/`** – Capa de Controlador
- **`compat.py`**: Clase `TaskControllerCompat` que:
  - Valida entradas de usuario antes de operaciones
  - Coordina entre vista y modelos
  - Maneja excepciones y propaga errores

#### 3. **Carpeta `views/`** – Capa de Vista
- **`launcher.py`**: Clase `Launcher` (ventana principal Tkinter) con:
  - Treeview para empleados (columnas: ID, Nombre, Email, País)
  - Treeview para tareas (columnas: ID, Descripción, Empleado, Estado)
  - Botones para operaciones CRUD (Add Employee, Add Task, Lookup, Delete, Refresh, Exit)
  - Métodos para refresh automático de datos

- **`ui_manager.py`**: Clase `UIManager` que:
  - Gestiona formularios especializados (EmployeeForm, TaskForm, LookupForm, DeleteForm)
  - Centraliza lógica de UI y callbacks
  - Sincroniza datos con la ventana principal

#### 4. **Carpeta `validators/`** – Validadores Reutilizables
- **`nonempty.py`**: Valida que campos no estén vacíos
- **`email.py`**: Valida formato de correo electrónico
- **`integer.py`**: Valida que valores sean números enteros
- **`exceptions.py`**: Excepciones específicas de validación

#### 5. **`task_db_app.py`** – Punto de Entrada
Script que:
- Inicializa `DatabaseManager`
- Crea `TaskControllerCompat`
- Lanza `Launcher` (interfaz gráfica)
- Implementa try-except-finally para manejo robusto de recursos

## Manejo de Errores

La aplicación implementa un sistema robusto de excepciones:

```python
# Excepciones personalizadas
try:
    controller.add_employee("Alice", "Smith", "Canada", "alice@example.com")
except ValidationError as e:
    messagebox.showerror("Validación", str(e))
except DatabaseError as e:
    messagebox.showerror("Base de Datos", str(e))
finally:
    # Recursos se liberan automáticamente
```

## Formularios Disponibles

1. **Add Employee**: Inserta nuevo empleado con validación de email
2. **Add Task**: Asigna tarea a empleado existente
3. **Lookup**: Busca empleado o tarea por ID
4. **Delete Employee**: Elimina empleado y opcionalmente sus tareas

## Cómo Ejecutar

### Opción 1: Directamente en VS Code
- Abrir `task_db_app.py`
- Presionar `F5` o hacer clic en "Run"

## Flujo de Datos

```
Vista (Tkinter GUI - Launcher)
    ↓ (usuario ingresa datos en formularios)
UIManager (gestiona formularios y callbacks)
    ↓ (datos del usuario)
Controlador (TaskControllerCompat - validaciones, lógica)
    ↓ (datos validados)
Modelos (EmployeeModel, TaskModel, BacklogModel)
    ↓ (queries SQL parametrizadas)
DatabaseConnection (SQLite)
    ↓ (datos persistidos)
Vista (refresh automático de Treeviews)
```

## Características de Diseño

- ✅ **Separación de Responsabilidades**: Cada módulo tiene un propósito específico
- ✅ **Reutilizable**: Los modelos pueden usarse independientemente de la GUI
- ✅ **Escalable**: Fácil agregar nuevas entidades (crear nuevo `*_model.py`)
- ✅ **Documentado**: Docstrings Google Style en todas las clases y métodos
- ✅ **Testeable**: Lógica desacoplada facilita pruebas unitarias
- ✅ **Seguro**: Consultas parametrizadas previenen SQL injection
- ✅ **Modular**: Validators, controllers y views completamente desacoplados
- ✅ **Type Hints**: Anotaciones de tipo para mejor legibilidad

---

# Sistema de Logging Distribuido

## ¿Qué es?

Sistema cliente-servidor que recibe mensajes de múltiples clientes y los registra centralizadamente en archivos de log con información de origen, timestamps y contenido.

## Inicio Rápido

### 1️⃣ Terminal 1 - Inicia el servidor

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

### 2️⃣ Terminal 2 - Conecta un cliente (Modo Interactivo)

```bash
python client.py
```

Luego puedes escribir mensajes:
```
>>> Error en base de datos
>>> Usuario autenticado
>>> exit
```

### 3️⃣ (Alternativo) Terminal 2 - Envía un mensaje único

```bash
python client.py "Mi mensaje de prueba"
```

### 4️⃣ (Alternativo) Ejecuta la demostración

```bash
python demo_logging.py
```

Esto ejecutará varios clientes automáticamente enviando mensajes.

## Archivos Principales del Sistema de Logging

| Archivo | Descripción |
|---------|-------------|
| `server.py` | Servidor TCP que recibe y registra mensajes |
| `client.py` | Cliente que envía mensajes al servidor |
| `demo_logging.py` | Script de demostración con múltiples escenarios |

## Archivos de Log Creados

- `logs/server.log` - Eventos del servidor (conexiones, desconexiones)
- `logs/client_messages.log` - Mensajes de clientes con información de origen

## Ejemplo de Formato de Logs

**server.log:**
```
2026-05-12 08:48:57 | SERVER | INFO | Servidor iniciado en localhost:9999
2026-05-12 08:48:57 | SERVER | INFO | Cliente #1 conectado desde ('127.0.0.1', 54618)
2026-05-12 08:48:57 | SERVER | INFO | Mensaje recibido de Cliente #1: Aplicación iniciada
```

**client_messages.log:**
```
2026-05-12 08:48:57 | CLIENT MESSAGE | [Cliente #1 | 127.0.0.1:54618] Aplicación iniciada
```

## Características del Sistema de Logging

✅ Múltiples clientes simultáneos  
✅ Timestamps automáticos en cada mensaje  
✅ Identificación de cliente (IP y puerto)  
✅ Logging a archivo y consola  
✅ Manejo robusto de errores  
✅ Sin dependencias externas  
✅ Protocolo TCP confiable  
✅ Threads para manejo concurrente

## Configuración del Sistema de Logging

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

### Métodos principales

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

## Ejemplo de Uso Programático del Logging

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

## Información Técnica del Sistema de Logging

| Aspecto | Valor |
|--------|-------|
| **Protocolo** | TCP |
| **Puerto por defecto** | 9999 (configurable) |
| **Conexiones simultáneas** | Sin límite (limitado por sistema) |
| **Tamaño máximo de mensaje** | 1024 bytes |
| **Conexiones en cola** | 5 máximo |

## Manejo de Errores en el Logging

El sistema maneja los siguientes casos:

- **Servidor no disponible**: El cliente reporta error de conexión
- **Cliente desconectado abruptamente**: El servidor registra la desconexión
- **Mensajes vacíos**: Se ignoran
- **Comando 'exit'**: Desconexión limpia

## Mejoras Futuras del Sistema de Logging

- [ ] Autenticación de clientes
- [ ] Cifrado de comunicaciones (SSL/TLS)
- [ ] Rotación de archivos de log
- [ ] Base de datos para almacenar logs
- [ ] Dashboard web para ver logs en tiempo real
- [ ] Diferentes niveles de log (DEBUG, INFO, WARNING, ERROR)
- [ ] Filtrado de mensajes
- [ ] Compresión de logs antiguos


