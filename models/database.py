"""Gestión de conexión a la base de datos SQLite.

Proporciona la clase DatabaseConnection que encapsula la lógica de conexión
y transacciones con SQLite, implementando patrones de manejo de errores robusto.
"""

import os
import sqlite3
from models.exceptions import DatabaseError
from utils.decorators import timer, handle_database_errors

DB_FILENAME = os.path.join(os.path.dirname(__file__), '..', 'tasks.db')


class DatabaseConnection:
    """Gestiona la conexión a la base de datos SQLite.

    Proporciona métodos para conectar, desconectar y ejecutar operaciones
    en la base de datos con manejo centralizado de errores.

    Attributes:
        db_path (str): Ruta al archivo de base de datos SQLite.
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
        cur (sqlite3.Cursor): Cursor para ejecutar comandos SQL.

    Example:
        >>> db = DatabaseConnection()
        >>> db.execute("SELECT * FROM employee")
        [(...), (...)]
        >>> db.close()
    """

    def __init__(self, db_path: str | None = None):
        """Inicializa la conexión a la base de datos.

        Args:
            db_path (str, optional): Ruta a la base de datos SQLite. Si no se proporciona,
                usa la ruta por defecto (tasks.db en el directorio padre).

        Raises:
            DatabaseError: Si no se puede establecer la conexión a la base de datos.
        """
        self.db_path = db_path or DB_FILENAME
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()
        except sqlite3.Error as exc:
            raise DatabaseError(f"No se pudo conectar a {self.db_path}: {exc}")

    @timer
    @handle_database_errors
    def execute(self, query: str, params: tuple | None = None) -> list:
        """Ejecuta una consulta SELECT y retorna los resultados.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, optional): Parámetros para la consulta parametrizada.

        Returns:
            list: Lista de tuplas con los resultados de la consulta.

        Raises:
            DatabaseError: Si falla la ejecución de la consulta.
        """
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            return self.cur.fetchall()
        except sqlite3.Error as exc:
            raise DatabaseError(f"Error al ejecutar consulta: {exc}")

    @timer
    @handle_database_errors
    def execute_one(self, query: str, params: tuple | None = None) -> tuple | None:
        """Ejecuta una consulta SELECT y retorna solo el primer resultado.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, optional): Parámetros para la consulta parametrizada.

        Returns:
            tuple | None: Primera fila de resultados o None si no hay resultados.

        Raises:
            DatabaseError: Si falla la ejecución de la consulta.
        """
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            return self.cur.fetchone()
        except sqlite3.Error as exc:
            raise DatabaseError(f"Error al ejecutar consulta: {exc}")

    @timer
    @handle_database_errors
    def execute_insert(self, query: str, params: tuple) -> int:
        """Ejecuta una consulta INSERT y retorna el ID del registro insertado.

        Args:
            query (str): Consulta INSERT a ejecutar.
            params (tuple): Parámetros para la consulta.

        Returns:
            int: ID autoincremental del registro insertado (lastrowid).

        Raises:
            DatabaseError: Si falla la inserción.
        """
        try:
            self.cur.execute(query, params)
            self.conn.commit()
            lastrowid = self.cur.lastrowid
            if lastrowid is None:
                raise DatabaseError("No se pudo obtener el ID del registro insertado")
            return int(lastrowid)
        except sqlite3.Error as exc:
            self.conn.rollback()
            raise DatabaseError(f"Error al insertar: {exc}")

    @timer
    @handle_database_errors
    def execute_update(self, query: str, params: tuple) -> int:
        """Ejecuta una consulta UPDATE o DELETE.

        Args:
            query (str): Consulta UPDATE/DELETE a ejecutar.
            params (tuple): Parámetros para la consulta.

        Returns:
            int: Número de filas afectadas.

        Raises:
            DatabaseError: Si falla la operación.
        """
        try:
            self.cur.execute(query, params)
            self.conn.commit()
            return self.cur.rowcount
        except sqlite3.Error as exc:
            self.conn.rollback()
            raise DatabaseError(f"Error al actualizar/eliminar: {exc}")

    @timer
    @handle_database_errors
    def executescript(self, script: str) -> None:
        """Ejecuta un script SQL (múltiples instrucciones).

        Args:
            script (str): Script SQL a ejecutar.

        Raises:
            DatabaseError: Si falla la ejecución del script.
        """
        try:
            self.cur.executescript(script)
            self.conn.commit()
        except sqlite3.Error as exc:
            raise DatabaseError(f"Error al ejecutar script: {exc}")

    def close(self) -> None:
        """Cierra la conexión a la base de datos.

        Libera los recursos asignados a la conexión. Debe llamarse antes de
        finalizar la aplicación para evitar fugas de recursos.
        """
        if hasattr(self, 'conn') and self.conn:
            try:
                self.conn.close()
            except sqlite3.Error:
                pass
