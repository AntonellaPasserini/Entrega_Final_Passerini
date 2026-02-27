# Instrucciones breves de uso

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
│   └── compat.py              # Controlador TaskControllerCompat
├── views/                     # Carpeta de vistas
│   ├── __init__.py
│   ├── launcher.py            # Ventana principal (Launcher)
│   └── ui_manager.py          # Gestor centralizado de UI
├── validators/                # Carpeta de validadores
│   ├── __init__.py
│   ├── nonempty.py            # Validación de campos no vacíos
│   ├── email.py               # Validación de formato email
│   ├── integer.py             # Validación de números enteros
│   └── exceptions.py          # Excepciones de validación
├── task_db_app.py             # Punto de entrada de la aplicación
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

### Opción 1: Terminal/PowerShell
```bash
cd c:\Users\antonella.passerini\Entrega_Final_Passerini
python task_db_app.py
```

### Opción 2: Directamente en VS Code
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


