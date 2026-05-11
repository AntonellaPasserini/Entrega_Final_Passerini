"""Modelo de datos para la entidad Task.

Implementa todas las operaciones CRUD y consultas especializadas
para la gestión de tareas en la base de datos.
"""

from datetime import datetime
from models.database import DatabaseConnection
from models.exceptions import DatabaseError
from utils.decorators import require_db_connection, timer, handle_database_errors, cache_result


class TaskModel:
    """Gestiona las operaciones de tareas en la base de datos.

    Proporciona métodos para crear, recuperar, actualizar y eliminar tareas,
    incluyendo consultas combinadas con empleados y operaciones en backlog.

    Attributes:
        db (DatabaseConnection): Instancia de conexión a la base de datos.

    Example:
        >>> db = DatabaseConnection()
        >>> task_model = TaskModel(db)
        >>> task_id = task_model.add_task(1, "Preparar reporte", "todo")
        >>> task = task_model.get_by_id(task_id)
    """

    def __init__(self, db: DatabaseConnection):
        """Inicializa el modelo de tareas.

        Args:
            db (DatabaseConnection): Instancia de conexión a la base de datos.
        """
        self.db = db

    @require_db_connection
    @timer
    @handle_database_errors
    def add_task(
        self, emp_id: int, description: str, status: str = "todo"
    ) -> int | None:
        """Inserta una nueva tarea en la base de datos.

        Crea un registro en la tabla `tasks` asignado a un empleado específico.
        El inicio (start_time) se establece automáticamente al momento actual.

        Args:
            emp_id (int): ID del empleado al que se asigna la tarea.
            description (str): Descripción de la tarea.
            status (str, optional): Estado inicial de la tarea. Por defecto 'todo'.
                Valores típicos: 'todo', 'in_progress', 'finished'.

        Returns:
            int | None: ID autoincremental de la tarea creada.

        Raises:
            DatabaseError: Si falla la inserción en la base de datos.

        Example:
            >>> task_id = task_model.add_task(1, "Preparar reporte mensual", "todo")
            >>> print(task_id)
            1
        """
        start_iso = datetime.now().isoformat()
        try:
            task_id = self.db.execute_insert(
                "INSERT INTO tasks (employee_id, description, status, start_time, finish_time) VALUES (?, ?, ?, ?, ?)",
                (emp_id, description, status, start_iso, None),
            )
            return task_id
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    def get_by_id(self, task_id: int) -> tuple | None:
        """Recupera los datos de una tarea por su ID.

        Args:
            task_id (int): ID de la tarea a recuperar.

        Returns:
            tuple | None: Tupla (id, employee_id, description, status, start_time, finish_time),
                o None si la tarea no existe.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> task = task_model.get_by_id(1)
            >>> print(task)
            (1, 1, 'Preparar reporte', 'todo', '2026-02-26T10:30:00', None)
        """
        try:
            return self.db.execute_one(
                "SELECT id, employee_id, description, status, start_time, finish_time FROM tasks WHERE id = ?",
                (task_id,),
            )
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    @cache_result
    def get_all(self) -> list[tuple]:
        """Recupera todas las tareas de la base de datos.

        Nota: Este método usa caching para mejorar rendimiento.
        Returns:
            list[tuple]: Lista de tuplas (id, employee_id, description, status, start_time, finish_time).

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> tasks = task_model.get_all()
            >>> for task in tasks:
            ...     print(task)
        """
        try:
            return self.db.execute(
                "SELECT id, employee_id, description, status, start_time, finish_time FROM tasks"
            )
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    def get_by_employee(self, emp_id: int) -> list[dict]:
        """Obtiene todas las tareas asignadas a un empleado.

        Consulta la vista employee_tasks_view para recuperar las tareas
        ordenadas por fecha de inicio (descendente).

        Args:
            emp_id (int): ID del empleado cuyas tareas se buscan.

        Returns:
            list[dict]: Lista de diccionarios con campos task_id, employee_id,
                employee_name, description, status, start_time, finish_time.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> tasks = task_model.get_by_employee(1)
            >>> for task in tasks:
            ...     print(task['description'], task['status'])
        """
        try:
            rows = self.db.execute(
                """
                SELECT task_id, employee_id, employee_name, description, status, start_time, finish_time
                FROM employee_tasks_view
                WHERE employee_id = ?
                ORDER BY start_time DESC
                """,
                (emp_id,),
            )
        except DatabaseError:
            raise

        tasks = []
        for row in rows:
            start = datetime.fromisoformat(row[5]) if row[5] else None
            finish = datetime.fromisoformat(row[6]) if row[6] else None
            tasks.append(
                {
                    "task_id": row[0],
                    "employee_id": row[1],
                    "employee_name": row[2],
                    "description": row[3],
                    "status": row[4],
                    "start_time": start,
                    "finish_time": finish,
                }
            )
        return tasks

    @require_db_connection
    @timer
    @handle_database_errors
    @cache_result
    def get_all_with_employee(self) -> list[tuple]:
        """Recupera todas las tareas con el nombre del empleado asignado.

        Realiza un LEFT JOIN entre tasks y employee para incluir el nombre
        del empleado en lugar de solo su ID. Se usa para poblar la tabla
        de tareas en la interfaz gráfica.
        Nota: Este método usa caching para mejorar rendimiento.

        Returns:
            list[tuple]: Lista de tuplas (task_id, description, status, employee_name).

        Raises:
            DatabaseError: Si ocurre un error al consultar la base de datos.

        Example:
            >>> tasks = task_model.get_all_with_employee()
            >>> for task in tasks:
            ...     print(f"{task[1]} - {task[3]}")
        """
        try:
            return self.db.execute(
                """
                SELECT t.id, t.description, t.status, e.name
                FROM tasks t
                LEFT JOIN employee e ON t.employee_id = e.id
                """
            )
        except DatabaseError:
            raise

    def delete(self, task_id: int) -> None:
        """Elimina una tarea de la base de datos.

        Borra el registro de la tarea y su entrada asociada en backlog.

        Args:
            task_id (int): ID de la tarea a eliminar.

        Raises:
            DatabaseError: Si falla la eliminación en la base de datos.

        Example:
            >>> task_model.delete(1)
        """
        try:
            self.db.execute_update(
                "DELETE FROM backlog WHERE task_id = ?", (task_id,)
            )
            self.db.execute_update(
                "DELETE FROM tasks WHERE id = ?", (task_id,)
            )
        except DatabaseError:
            raise

    def delete_by_employee(self, emp_id: int) -> int:
        """Elimina todas las tareas asignadas a un empleado.

        También elimina las entradas asociadas en backlog.

        Args:
            emp_id (int): ID del empleado cuyas tareas se eliminarán.

        Returns:
            int: Número de tareas eliminadas.

        Raises:
            DatabaseError: Si falla la operación.

        Example:
            >>> deleted_count = task_model.delete_by_employee(1)
            >>> print(f"Se eliminaron {deleted_count} tareas")
        """
        try:
            # Primero obtener los IDs de las tareas para eliminar backlog
            task_ids = self.db.execute(
                "SELECT id FROM tasks WHERE employee_id = ?", (emp_id,)
            )

            for (task_id,) in task_ids:
                self.db.execute_update(
                    "DELETE FROM backlog WHERE task_id = ?", (task_id,)
                )

            # Luego eliminar las tareas
            return self.db.execute_update(
                "DELETE FROM tasks WHERE employee_id = ?", (emp_id,)
            )
        except DatabaseError:
            raise

    def count_by_employee(self, emp_id: int) -> int:
        """Cuenta el número de tareas asignadas a un empleado.

        Args:
            emp_id (int): ID del empleado.

        Returns:
            int: Número de tareas del empleado.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> count = task_model.count_by_employee(1)
            >>> print(f"El empleado tiene {count} tareas")
        """
        try:
            result = self.db.execute_one(
                "SELECT COUNT(*) FROM tasks WHERE employee_id = ?", (emp_id,)
            )
            return result[0] if result else 0
        except DatabaseError:
            raise
