"""Controlador de empleados.

Maneja lógica de negocio para operaciones con empleados.
"""

from models.database_manager import DatabaseManager
from models.exceptions import DatabaseError, ValidationError
from validators import validate_email, validate_nonempty
from utils.decorators import log_execution


class EmployeeController:
    """Controlador de operaciones con empleados.

    Gestiona validaciones y coordinación de operaciones sobre empleados.

    Attributes:
        employee_model: Modelo de empleado del DatabaseManager.
        validator_email: Función para validar emails.
        validator_nonempty: Función para validar campos no-vacíos.

    Example:
        >>> manager = DatabaseManager()
        >>> controller = EmployeeController(manager)
        >>> controller.add_employee("John", "Doe", "USA", "john@example.com")
    """

    def __init__(self, manager: DatabaseManager):
        """Inicializa controlador de empleados.

        Args:
            manager (DatabaseManager): Gestor de base de datos.
        """
        self.employee_model = manager.employee

    @log_execution
    def add_employee(self, name: str, surname: str, country: str, email: str) -> str:
        """Agrega un nuevo empleado con validaciones.

        Valida que nombre no sea vacío y email tenga formato válido.

        Args:
            name (str): Nombre del empleado.
            surname (str): Apellido del empleado.
            country (str): País del empleado.
            email (str): Email del empleado.

        Returns:
            str: Mensaje de éxito con ID del empleado creado.

        Raises:
            ValidationError: Si datos no pasan validaciones.
            DatabaseError: Si ocurre error en base de datos.

        Example:
            >>> controller.add_employee("John", "Doe", "USA", "john@example.com")
            'Employee added with id 1.'
        """
        if not validate_nonempty(name):
            raise ValidationError("Name cannot be empty.")
        if not validate_email(email):
            raise ValidationError("Email looks invalid.")
        try:
            emp_id = self.employee_model.add_employee(name, surname, country, email)
            return f"Employee added with id {emp_id}."
        except DatabaseError:
            raise

    @log_execution
    def lookup_employee(self, emp_id: int) -> tuple:
        """Busca un empleado por su ID.

        Args:
            emp_id (int): ID del empleado a buscar.

        Returns:
            tuple: Datos del empleado (id, name, surname, email, country).

        Raises:
            ValidationError: Si empleado no existe.

        Example:
            >>> controller.lookup_employee(1)
            (1, 'John', 'Doe', 'john@example.com', 'USA')
        """
        emp = self.employee_model.get_by_id(emp_id)
        if not emp:
            raise ValidationError(f"No employee with id {emp_id}.")
        return emp

    @log_execution
    def get_all_employees(self) -> list:
        """Obtiene todos los empleados.

        Returns:
            list: Lista de tuples con datos de empleados.

        Example:
            >>> employees = controller.get_all_employees()
        """
        return self.employee_model.get_all()

    @log_execution
    def delete_employee(self, emp_id: int) -> str:
        """Elimina un empleado por su ID.

        Args:
            emp_id (int): ID del empleado a eliminar.

        Returns:
            str: Mensaje de éxito.

        Raises:
            ValidationError: Si empleado no existe.
            DatabaseError: Si ocurre error al eliminar.

        Example:
            >>> controller.delete_employee(1)
            'Employee 1 deleted.'
        """
        if not self.employee_model.exists(emp_id):
            raise ValidationError(f"No employee with id {emp_id}.")
        self.employee_model.delete(emp_id)
        return f"Employee {emp_id} deleted."

    def employee_exists(self, emp_id: int) -> bool:
        """Verifica si un empleado existe.

        Args:
            emp_id (int): ID del empleado a verificar.

        Returns:
            bool: True si existe, False en caso contrario.

        Example:
            >>> controller.employee_exists(1)
            True
        """
        return self.employee_model.exists(emp_id)
