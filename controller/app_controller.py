"""Controlador centralizado de aplicación.

Orquesta todas las operaciones de control de la aplicación.
"""

from models.database_manager import DatabaseManager
from controller.employee_controller import EmployeeController
from controller.task_controller import TaskController


class AppController:
    """Controlador centralizado de la aplicación.

    Orquestador que coordina controladores de empleados, tareas y otros.
    Implementa el patrón Facade para simplificar acceso a la lógica de negocio.

    Attributes:
        manager (DatabaseManager): Gestor de base de datos.
        employee (EmployeeController): Controlador de empleados.
        task (TaskController): Controlador de tareas.

    Example:
        >>> manager = DatabaseManager()
        >>> app_controller = AppController(manager)
        >>> app_controller.employee.add_employee("John", "Doe", "USA", "john@example.com")
    """

    def __init__(self, manager: DatabaseManager):
        """Inicializa controlador centralizado.

        Args:
            manager (DatabaseManager): Instancia del gestor de base de datos.
        """
        self.manager = manager
        self.employee = EmployeeController(manager)
        self.task = TaskController(manager)

    def get_combined_data(self) -> tuple:
        """Obtiene listas de empleados y tareas para visualización.

        Recupera todos los empleados y tareas para mostrar en la interfaz.

        Returns:
            tuple: (empleados, tareas) con datos combinados.

        Example:
            >>> employees, tasks = app_controller.get_combined_data()
        """
        return self.manager.get_combined_data()

    def close(self):
        """Cierra la conexión con la base de datos.

        Debe llamarse al finalizar la aplicación.

        Example:
            >>> app_controller.close()
        """
        self.manager.close()


# Compatibilidad con código anterior - alias para TaskController
def TaskController_Legacy(manager: DatabaseManager):
    """Wrapper para compatibilidad con código anterior.

    Retorna AppController que mantiene la interfaz original.

    Args:
        manager (DatabaseManager): Gestor de base de datos.

    Returns:
        AppController: Controlador centralizado.
    """
    return AppController(manager)
