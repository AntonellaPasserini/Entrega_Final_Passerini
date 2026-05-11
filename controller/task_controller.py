"""Controlador de tareas.

Maneja lógica de negocio para operaciones con tareas.
"""

from models.database_manager import DatabaseManager
from models.exceptions import DatabaseError, ValidationError
from validators import validate_int, validate_nonempty
from utils.decorators import log_execution


class TaskController:
    """Controlador de operaciones con tareas.

    Gestiona validaciones y coordinación de operaciones sobre tareas.

    Attributes:
        task_model: Modelo de tarea del DatabaseManager.
        employee_model: Modelo de empleado del DatabaseManager.

    Example:
        >>> manager = DatabaseManager()
        >>> controller = TaskController(manager)
        >>> controller.add_task(1, "Complete project", "In Progress")
    """

    def __init__(self, manager: DatabaseManager):
        """Inicializa controlador de tareas.

        Args:
            manager (DatabaseManager): Gestor de base de datos.
        """
        self.task_model = manager.task
        self.employee_model = manager.employee

    @log_execution
    def add_task(self, emp_id: int, description: str, status: str) -> str:
        """Agrega una nueva tarea con validaciones.

        Valida que empleado exista y descripción no esté vacía.

        Args:
            emp_id (int): ID del empleado asignado.
            description (str): Descripción de la tarea.
            status (str): Estado inicial de la tarea.

        Returns:
            str: Mensaje de éxito con ID de la tarea creada.

        Raises:
            ValidationError: Si datos no pasan validaciones.
            DatabaseError: Si ocurre error en base de datos.

        Example:
            >>> controller.add_task(1, "Complete project", "In Progress")
            'Task added for employee 1 (id 1).'
        """
        if not validate_int(str(emp_id)):
            raise ValidationError("Employee ID must be integer")
        if not self.employee_model.exists(emp_id):
            raise ValidationError(f"No employee with id {emp_id}.")
        if not validate_nonempty(description):
            raise ValidationError("Description cannot be empty.")
        try:
            task_id = self.task_model.add_task(emp_id, description, status)
            return f"Task added for employee {emp_id} (id {task_id})."
        except DatabaseError:
            raise

    @log_execution
    def lookup_task(self, task_id: int) -> tuple:
        """Busca una tarea por su ID con nombre de empleado.

        Args:
            task_id (int): ID de la tarea a buscar.

        Returns:
            tuple: (task_data, employee_name) con datos de tarea y empleado.

        Raises:
            ValidationError: Si tarea no existe.

        Example:
            >>> task, emp_name = controller.lookup_task(1)
        """
        if not validate_int(str(task_id)):
            raise ValidationError("Task ID must be integer")
        task = self.task_model.get_by_id(task_id)
        if not task:
            raise ValidationError(f"No task with id {task_id}.")
        emp = self.employee_model.get_by_id(task[1])
        emp_name = emp[1] if emp else "Unknown"
        return task, emp_name

    @log_execution
    def get_tasks(self, emp_id: int) -> list:
        """Obtiene todas las tareas de un empleado.

        Args:
            emp_id (int): ID del empleado.

        Returns:
            list: Lista de diccionarios con datos de tareas.

        Raises:
            ValidationError: Si ID no es entero.

        Example:
            >>> tasks = controller.get_tasks(1)
        """
        if not validate_int(str(emp_id)):
            raise ValidationError("Employee ID must be integer")
        return self.task_model.get_by_employee(emp_id)

    @log_execution
    def get_all_tasks(self) -> list:
        """Obtiene todas las tareas con datos de empleados.

        Returns:
            list: Lista de tuples con datos de tareas y empleados.

        Example:
            >>> tasks = controller.get_all_tasks()
        """
        return self.task_model.get_all_with_employee()

    @log_execution
    def delete_task(self, task_id: int) -> str:
        """Elimina una tarea por su ID.

        Args:
            task_id (int): ID de la tarea a eliminar.

        Returns:
            str: Mensaje de éxito.

        Raises:
            ValidationError: Si tarea no existe.
            DatabaseError: Si ocurre error al eliminar.

        Example:
            >>> controller.delete_task(1)
            'Task 1 deleted.'
        """
        if not validate_int(str(task_id)):
            raise ValidationError("Task ID must be integer")
        task = self.task_model.get_by_id(task_id)
        if not task:
            raise ValidationError(f"No task with id {task_id}.")
        self.task_model.delete(task_id)
        return f"Task {task_id} deleted."

    def count_employee_tasks(self, emp_id: int) -> int:
        """Cuenta cuántas tareas tiene un empleado.

        Args:
            emp_id (int): ID del empleado.

        Returns:
            int: Número de tareas del empleado.

        Example:
            >>> count = controller.count_employee_tasks(1)
        """
        if not validate_int(str(emp_id)):
            raise ValidationError("Employee ID must be integer")
        return self.task_model.count_by_employee(emp_id)
