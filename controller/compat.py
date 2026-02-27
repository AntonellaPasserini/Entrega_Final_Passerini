"""Wrapper de compatibilidad para AppController.

Proporciona interfaz compatible con código legacy.
"""

from controller import AppController
from validators import validate_int


class TaskControllerCompat(AppController):
    """Versión compatible de TaskController que hereda de AppController.

    Mantiene la interfaz original de TaskController pero usa AppController internamente.

    Example:
        >>> manager = DatabaseManager()
        >>> controller = TaskControllerCompat(manager)
        >>> controller.add_employee("John", "Doe", "USA", "john@example.com")
    """

    def __init__(self, manager):
        """Inicializa con el gestor de BD.

        Args:
            manager (DatabaseManager): Gestor de base de datos.
        """
        super().__init__(manager)
        # Copiar referencias para compatibilidad directa
        self.employee_model = manager.employee
        self.task_model = manager.task
        self.backlog = manager.backlog

    def add_employee(self, name, surname, country, email):
        """Compatible con TaskController antiguo.

        Args:
            name (str): Nombre.
            surname (str): Apellido.
            country (str): País.
            email (str): Email.

        Returns:
            str: Mensaje de éxito.
        """
        return self.employee.add_employee(name, surname, country, email)

    def add_task(self, emp_id, description, status):
        """Compatible con TaskController antiguo.

        Args:
            emp_id (int): ID del empleado.
            description (str): Descripción.
            status (str): Estado.

        Returns:
            str: Mensaje de éxito.
        """
        return self.task.add_task(emp_id, description, status)

    def lookup_employee(self, emp_id):
        """Compatible con TaskController antiguo.

        Args:
            emp_id (int): ID del empleado.

        Returns:
            tuple: Datos del empleado.
        """
        return self.employee.lookup_employee(emp_id)

    def lookup_task(self, task_id):
        """Compatible con TaskController antiguo.

        Args:
            task_id (int): ID de la tarea.

        Returns:
            tuple: (task, employee_name).
        """
        return self.task.lookup_task(task_id)

    def get_tasks(self, emp_id):
        """Compatible con TaskController antiguo.

        Args:
            emp_id (int): ID del empleado.

        Returns:
            list: Tareas del empleado.
        """
        return self.task.get_tasks(emp_id)

    def delete_employee_prompt(self, emp_id):
        """Compatible con TaskController antiguo.

        Args:
            emp_id (int): ID del empleado.

        Returns:
            bool: True si existe.
        """
        if not validate_int(str(emp_id)):
            from models.exceptions import ValidationError
            raise ValidationError("Employee ID must be integer")
        return self.employee.employee_exists(emp_id)

    def delete_employee(self, emp_id, delete_tasks=False):
        """Compatible con TaskController antiguo.

        Args:
            emp_id (int): ID del empleado.
            delete_tasks (bool): Eliminar tareas asociadas.

        Returns:
            str: Mensaje de éxito.
        """
        if delete_tasks:
            self.task_model.delete_by_employee(emp_id)
        return self.employee.delete_employee(emp_id)

    def obtener_datos_combinados(self):
        """Compatible con TaskController antiguo.

        Returns:
            tuple: (empleados, tareas).
        """
        return self.get_combined_data()

    def get_all_employees(self):
        """Obtiene todos los empleados.

        Returns:
            list: Lista de empleados.
        """
        return self.employee.get_all_employees()

    def get_all_tasks_combined(self):
        """Obtiene todas las tareas con empleados.

        Returns:
            list: Lista de tareas.
        """
        return self.task.get_all_tasks()
