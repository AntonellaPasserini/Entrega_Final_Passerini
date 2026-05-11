"""Modelo de datos para la entidad Employee.

Implementa todas las operaciones CRUD (Create, Read, Update, Delete)
específicas para empleados en la base de datos.
"""

from models.database import DatabaseConnection
from models.exceptions import DatabaseError, ValidationError
from utils.decorators import require_db_connection, timer, handle_database_errors, cache_result


class EmployeeModel:
    """Gestiona las operaciones de empleados en la base de datos.

    Proporciona métodos para crear, recuperar, actualizar y eliminar empleados,
    además de consultas especializadas para validaciones y búsquedas.

    Attributes:
        db (DatabaseConnection): Instancia de conexión a la base de datos.

    Example:
        >>> db = DatabaseConnection()
        >>> employee_model = EmployeeModel(db)
        >>> emp_id = employee_model.add_employee("Juan", "Gómez", "Colombia", "juan@example.com")
        >>> emp = employee_model.get_by_id(emp_id)
        >>> print(emp)
        (1, 'Juan', 'Gómez', 'Colombia', 'juan@example.com')
    """

    def __init__(self, db: DatabaseConnection):
        """Inicializa el modelo de empleados.

        Args:
            db (DatabaseConnection): Instancia de conexión a la base de datos.
        """
        self.db = db

    @require_db_connection
    @timer
    @handle_database_errors
    def add_employee(
        self, name: str, surname: str, country: str, email: str
    ) -> int | None:
        """Inserta un nuevo empleado en la base de datos.

        Crea un nuevo registro en la tabla `employee` con los datos proporcionados.
        Los valores se validan al nivel del controlador antes de llamar este método.

        Args:
            name (str): Nombre del empleado.
            surname (str): Apellido del empleado.
            country (str): País del empleado.
            email (str): Correo electrónico del empleado.

        Returns:
            int | None: ID autoincremental del empleado creado.

        Raises:
            DatabaseError: Si falla la inserción en la base de datos.

        Example:
            >>> emp_id = employee_model.add_employee("Alice", "Perez", "Canada", "alice@example.com")
            >>> print(emp_id)
            1
        """
        try:
            emp_id = self.db.execute_insert(
                "INSERT INTO employee (name, surname, country, email) VALUES (?, ?, ?, ?)",
                (name, surname, country, email),
            )
            return emp_id
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    def exists(self, emp_id: int) -> bool:
        """Verifica si un empleado existe en la base de datos.

        Args:
            emp_id (int): ID del empleado a verificar.

        Returns:
            bool: True si el empleado existe, False en caso contrario.

        Example:
            >>> employee_model.exists(1)
            True
            >>> employee_model.exists(999)
            False
        """
        try:
            result = self.db.execute_one(
                "SELECT 1 FROM employee WHERE id = ?", (emp_id,)
            )
            return result is not None
        except DatabaseError:
            return False

    @require_db_connection
    @timer
    @handle_database_errors
    def get_by_id(self, emp_id: int) -> tuple | None:
        """Recupera los datos de un empleado por su ID.

        Args:
            emp_id (int): ID del empleado a recuperar.

        Returns:
            tuple | None: Tupla (id, name, surname, country, email) del empleado,
                o None si no existe.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> emp = employee_model.get_by_id(1)
            >>> print(emp)
            (1, 'Alice', 'Perez', 'Canada', 'alice@example.com')
        """
        try:
            return self.db.execute_one(
                "SELECT id, name, surname, country, email FROM employee WHERE id = ?",
                (emp_id,),
            )
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    @cache_result
    def get_all(self) -> list[tuple]:
        """Recupera todos los empleados de la base de datos.

        Devuelve una lista de tuplas con la información de cada empleado.
        Se usa para poblar la tabla de empleados en la interfaz gráfica.
        Nota: Este método usa caching para mejorar rendimiento.

        Returns:
            list[tuple]: Lista de tuplas (id, name, surname, country, email).

        Raises:
            DatabaseError: Si ocurre un error al consultar la base de datos.

        Example:
            >>> employees = employee_model.get_all()
            >>> for emp in employees:
            ...     print(emp)
            (1, 'Alice', 'Perez', 'Canada', 'alice@example.com')
            (2, 'Juan', 'Gomez', 'Colombia', 'juan@example.com')
        """
        try:
            return self.db.execute(
                "SELECT id, name, surname, country, email FROM employee"
            )
        except DatabaseError:
            raise

    def delete(self, emp_id: int) -> None:
        """Elimina un empleado de la base de datos.

        Borra el registro del empleado. Las tareas asociadas deben manejarse
        a nivel del controlador antes de llamar este método.

        Args:
            emp_id (int): ID del empleado a eliminar.

        Raises:
            ValidationError: Si el empleado no existe.
            DatabaseError: Si falla la eliminación en la base de datos.

        Example:
            >>> employee_model.delete(1)
        """
        if not self.exists(emp_id):
            raise ValidationError(f"Empleado {emp_id} no existe")
        try:
            self.db.execute_update(
                "DELETE FROM employee WHERE id = ?", (emp_id,)
            )
        except DatabaseError:
            raise

    def get_by_email(self, email: str) -> tuple | None:
        """Busca un empleado por su correo electrónico.

        Args:
            email (str): Correo electrónico del empleado a buscar.

        Returns:
            tuple | None: Tupla (id, name, surname, country, email) si existe,
                None en caso contrario.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> emp = employee_model.get_by_email("alice@example.com")
            >>> print(emp)
            (1, 'Alice', 'Perez', 'Canada', 'alice@example.com')
        """
        try:
            return self.db.execute_one(
                "SELECT id, name, surname, country, email FROM employee WHERE email = ?",
                (email,),
            )
        except DatabaseError:
            raise
