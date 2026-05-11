"""Modelo de datos para la entidad Backlog.

Implementa las operaciones relacionadas con el backlog (prioridades y seguimiento).
"""

from datetime import datetime
from models.database import DatabaseConnection
from models.exceptions import DatabaseError
from utils.decorators import require_db_connection, timer, handle_database_errors, cache_result


class BacklogModel:
    """Gestiona las operaciones de backlog en la base de datos.

    El backlog se utiliza para gestionar prioridades y seguimiento
    de tareas que requieren especial atención o planificación futura.

    Attributes:
        db (DatabaseConnection): Instancia de conexión a la base de datos.

    Example:
        >>> db = DatabaseConnection()
        >>> backlog_model = BacklogModel(db)
        >>> backlog_id = backlog_model.add_to_backlog(1, priority=2)
    """

    def __init__(self, db: DatabaseConnection):
        """Inicializa el modelo de backlog.

        Args:
            db (DatabaseConnection): Instancia de conexión a la base de datos.
        """
        self.db = db

    @require_db_connection
    @timer
    @handle_database_errors
    def add_to_backlog(self, task_id: int, priority: int = 3) -> int | None:
        """Añade una tarea al backlog con prioridad especificada.

        Args:
            task_id (int): ID de la tarea a añadir al backlog.
            priority (int, optional): Prioridad de la tarea (1-5, donde 1 es más urgente).
                Por defecto 3 (prioridad media).

        Returns:
            int | None: ID del registro de backlog creado.

        Raises:
            DatabaseError: Si falla la inserción en la base de datos.

        Example:
            >>> backlog_id = backlog_model.add_to_backlog(1, priority=2)
            >>> print(backlog_id)
            1
        """
        created_at = datetime.now().isoformat()
        try:
            backlog_id = self.db.execute_insert(
                "INSERT INTO backlog (task_id, created_at, priority) VALUES (?, ?, ?)",
                (task_id, created_at, priority),
            )
            return backlog_id
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    def get_by_id(self, backlog_id: int) -> tuple | None:
        """Recupera un registro de backlog por su ID.

        Args:
            backlog_id (int): ID del registro de backlog.

        Returns:
            tuple | None: Tupla (id, task_id, created_at, priority) o None si no existe.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> backlog = backlog_model.get_by_id(1)
            >>> print(backlog)
            (1, 1, '2026-02-26T10:30:00', 2)
        """
        try:
            return self.db.execute_one(
                "SELECT id, task_id, created_at, priority FROM backlog WHERE id = ?",
                (backlog_id,),
            )
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    def get_by_task(self, task_id: int) -> tuple | None:
        """Busca un registro de backlog por el ID de la tarea.

        Args:
            task_id (int): ID de la tarea.

        Returns:
            tuple | None: Tupla (id, task_id, created_at, priority) o None si no existe.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> backlog = backlog_model.get_by_task(1)
            >>> print(backlog)
            (1, 1, '2026-02-26T10:30:00', 2)
        """
        try:
            return self.db.execute_one(
                "SELECT id, task_id, created_at, priority FROM backlog WHERE task_id = ?",
                (task_id,),
            )
        except DatabaseError:
            raise

    @require_db_connection
    @timer
    @handle_database_errors
    @cache_result
    def get_all(self) -> list[tuple]:
        """Recupera todos los registros de backlog.

        Nota: Este método usa caching para mejorar rendimiento.
        Returns:
            list[tuple]: Lista de tuplas (id, task_id, created_at, priority).

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> backlog_items = backlog_model.get_all()
            >>> for item in backlog_items:
            ...     print(item)
        """
        try:
            return self.db.execute(
                "SELECT id, task_id, created_at, priority FROM backlog ORDER BY priority ASC, created_at DESC"
            )
        except DatabaseError:
            raise

    def update_priority(self, backlog_id: int, new_priority: int) -> None:
        """Actualiza la prioridad de un registro de backlog.

        Args:
            backlog_id (int): ID del registro de backlog.
            new_priority (int): Nueva prioridad (1-5).

        Raises:
            DatabaseError: Si falla la actualización en la base de datos.

        Example:
            >>> backlog_model.update_priority(1, 1)
        """
        try:
            self.db.execute_update(
                "UPDATE backlog SET priority = ? WHERE id = ?",
                (new_priority, backlog_id),
            )
        except DatabaseError:
            raise

    def delete(self, backlog_id: int) -> None:
        """Elimina un registro de backlog.

        Args:
            backlog_id (int): ID del registro de backlog a eliminar.

        Raises:
            DatabaseError: Si falla la eliminación en la base de datos.

        Example:
            >>> backlog_model.delete(1)
        """
        try:
            self.db.execute_update(
                "DELETE FROM backlog WHERE id = ?", (backlog_id,)
            )
        except DatabaseError:
            raise

    def delete_by_task(self, task_id: int) -> None:
        """Elimina los registros de backlog asociados a una tarea.

        Args:
            task_id (int): ID de la tarea.

        Raises:
            DatabaseError: Si falla la eliminación en la base de datos.

        Example:
            >>> backlog_model.delete_by_task(1)
        """
        try:
            self.db.execute_update(
                "DELETE FROM backlog WHERE task_id = ?", (task_id,)
            )
        except DatabaseError:
            raise

    def get_high_priority(self, min_priority: int = 2) -> list[dict]:
        """Obtiene tareas en backlog con alta prioridad.

        Args:
            min_priority (int, optional): Prioridad mínima (más bajo = más urgente).
                Por defecto 2.

        Returns:
            list[dict]: Lista de diccionarios con información de tareas en backlog.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos.

        Example:
            >>> high_priority = backlog_model.get_high_priority(min_priority=2)
            >>> for item in high_priority:
            ...     print(item)
        """
        try:
            rows = self.db.execute(
                """
                SELECT b.id, b.task_id, t.description, b.priority, b.created_at
                FROM backlog b
                JOIN tasks t ON b.task_id = t.id
                WHERE b.priority <= ?
                ORDER BY b.priority ASC, b.created_at DESC
                """,
                (min_priority,),
            )
        except DatabaseError:
            raise

        items = []
        for row in rows:
            items.append(
                {
                    "backlog_id": row[0],
                    "task_id": row[1],
                    "description": row[2],
                    "priority": row[3],
                    "created_at": datetime.fromisoformat(row[4]),
                }
            )
        return items
