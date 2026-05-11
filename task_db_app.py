#!/usr/bin/env python3
"""Punto de entrada de la aplicación Task DB App con modelos separados.

Inicializa la arquitectura MVC:
    1. Crea una instancia del Gestor de BD (DatabaseManager).
    2. Inicializa la base de datos (tablas, vistas, datos de ejemplo).
    3. Crea el Controlador (TaskController).
    4. Lanza la Vista principal (Launcher).

Usage:
    python task_db_app.py
"""

from models import DatabaseManager, DatabaseError
from controller.compat import TaskControllerCompat
from views import Launcher, UIManager
from validators import nonempty, email, integer, exceptions as validator_exceptions
from utils.decorators import log_execution, handle_database_errors


# Agrupar las validaciones disponibles en un único objeto que se pasará a la UI
validaciones = {
    "nonempty": nonempty,
    "email": email,
    "integer": integer,
    "exceptions": validator_exceptions,
}


@log_execution
@handle_database_errors
def main():
    """Inicializa y ejecuta la aplicación de escritorio.

    Realiza el siguiente flujo:
        1. Crea el gestor centralizado de base de datos.
        2. Genera las tablas (si no existen).
        3. Puebla con datos de ejemplo (si están vacías).
        4. Crea la vista SQL para JOIN de empleados/tareas.
        5. Instancia el controlador y la ventana principal.
        6. Inicia el bucle de eventos de la GUI.

    Si ocurre un error crítico (conexión fallida, etc.),
    imprime el mensaje en consola y cierra los recursos.
    """
    manager = None
    try:
        # Crear gestor de base de datos con la nueva arquitectura modular
        manager = DatabaseManager()
        manager.initialize()

        # Crear controlador centralizado
        controller = TaskControllerCompat(manager)

        # Crear aplicación gráfica
        app = Launcher(controller, validaciones, UIManager(root=None, controller=controller, validator=validaciones))
        app.ui_manager.root = app  # Asignar la referencia de app al UIManager
        app.mainloop()

    except DatabaseError as exc:
        print(f"Error de base de datos: {exc}")
    except Exception as exc:
        print(f"Se produjo un error inesperado: {exc}")
    finally:
        # Cerrar la conexión si existe
        if manager:
            try:
                manager.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
