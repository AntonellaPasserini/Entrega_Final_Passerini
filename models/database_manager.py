"""Gestor centralizado de la base de datos.

Orquesta la creación de tablas, inicialización de datos y proporciona
una interfaz unificada para acceder a todos los modelos.
"""

from datetime import datetime, timedelta
from models.database import DatabaseConnection
from models.exceptions import DatabaseError
from models.employee_model import EmployeeModel
from models.task_model import TaskModel
from models.backlog_model import BacklogModel
from utils.decorators import timer, log_execution


class DatabaseManager:
    """Gestor centralizado que coordina todas las operaciones de base de datos.

    Encapsula la creación de tablas, inicialización de datos y proporciona
    acceso a los modelos específicos de cada entidad (Employee, Task, Backlog).
    Implementa el patrón Facade para simplificar la interfaz de la base de datos.

    Attributes:
        db (DatabaseConnection): Conexión a la base de datos.
        employee (EmployeeModel): Modelo para operaciones de empleados.
        task (TaskModel): Modelo para operaciones de tareas.
        backlog (BacklogModel): Modelo para operaciones de backlog.

    Example:
        >>> manager = DatabaseManager()
        >>> manager.initialize()
        >>> emp_id = manager.employee.add_employee("Juan", "Gómez", "Colombia", "juan@example.com")
        >>> manager.close()
    """

    def __init__(self, db_path: str | None = None):
        """Inicializa el gestor de base de datos.

        Args:
            db_path (str, optional): Ruta a la base de datos SQLite.
                Si no se proporciona, usa la ruta por defecto.

        Raises:
            DatabaseError: Si no se puede establecer la conexión.
        """
        self.db = DatabaseConnection(db_path)
        self.employee = EmployeeModel(self.db)
        self.task = TaskModel(self.db)
        self.backlog = BacklogModel(self.db)

    @timer
    @log_execution
    def initialize(self) -> None:
        """Inicializa la base de datos creando tablas y datos de ejemplo.

        Llamar este método una única vez al arrancar la aplicación.
        Crea las tablas si no existen y puebla con datos de ejemplo.

        Raises:
            DatabaseError: Si ocurre un error durante la inicialización.

        Example:
            >>> manager = DatabaseManager()
            >>> manager.initialize()
        """
        try:
            self.create_tables()
            self.seed_data()
            self.create_view()
        except DatabaseError:
            raise

    @timer
    def create_tables(self) -> None:
        """Crea las tablas principales de la base de datos.

        Genera las tablas `employee`, `tasks` y `backlog` si no existen.
        Usa la cláusula IF NOT EXISTS para permitir múltiples ejecuciones.

        Raises:
            DatabaseError: Si ocurre un error al crear las tablas.

        Example:
            >>> manager.create_tables()
        """
        script = """
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    country TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    start_time TEXT NOT NULL,
    finish_time TEXT,
    FOREIGN KEY(employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS backlog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    created_at TEXT NOT NULL,
    priority INTEGER DEFAULT 3,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);
"""
        try:
            self.db.executescript(script)
        except DatabaseError:
            raise

    @timer
    def seed_data(self) -> None:
        """Inserta datos de ejemplo en las tablas vacías.

        Puebla las tablas employee, tasks y backlog con datos de demostración
        si no contienen registros. Se ejecuta solo una vez al inicializar la app.

        Raises:
            DatabaseError: Si ocurre un error durante la inserción de datos.

        Example:
            >>> manager.seed_data()
        """
        try:
            # Verificar si employee está vacía
            if not self.employee.get_all():
                employees = [
                    ("Alice", "Perez", "Canada", "alice.perez@example.com"),
                    ("Juan", "Gomez", "Colombia", "juan.gomez@example.com"),
                    ("Maria", "Lopez", "Argentina", "maria.lopez@example.com"),
                    ("Karthik", "Raman", "India", "karthik.raman@example.com"),
                ]
                for name, surname, country, email in employees:
                    self.employee.add_employee(name, surname, country, email)

            # Verificar si tasks está vacía
            if not self.task.get_all():
                now = datetime.now()
                tasks = [
                    (
                        1,
                        "Prepare monthly report",
                        "finished",
                        (now - timedelta(days=3)).isoformat(),
                        (now - timedelta(days=2)).isoformat(),
                    ),
                    (
                        1,
                        "Update client spreadsheet",
                        "in_progress",
                        (now - timedelta(hours=5)).isoformat(),
                        None,
                    ),
                    (
                        2,
                        "Set up meeting",
                        "finished",
                        (now - timedelta(days=1)).isoformat(),
                        (now - timedelta(days=1, hours=-1)).isoformat(),
                    ),
                    (
                        3,
                        "Research new library",
                        "todo",
                        now.isoformat(),
                        None,
                    ),
                    (
                        4,
                        "Develop project plan",
                        "in_progress",
                        (now - timedelta(hours=2)).isoformat(),
                        None,
                    ),
                    (
                        4,
                        "Complete code review",
                        "finished",
                        (now - timedelta(days=2)).isoformat(),
                        (now - timedelta(days=1, hours=20)).isoformat(),
                    ),
                ]
                for emp_id, desc, status, start, finish in tasks:
                    self.db.execute_insert(
                        "INSERT INTO tasks (employee_id, description, status, start_time, finish_time) VALUES (?, ?, ?, ?, ?)",
                        (emp_id, desc, status, start, finish),
                    )

            # Verificar si backlog está vacío
            if not self.backlog.get_all():
                created_at = datetime.now().isoformat()
                all_tasks = self.task.get_all()
                if all_tasks:
                    first_task_id = all_tasks[0][0]
                    self.backlog.add_to_backlog(first_task_id, priority=2)

        except DatabaseError:
            raise

    @timer
    def create_view(self) -> None:
        """Crea una vista SQL que une empleados con sus tareas.

        Define la vista `employee_tasks_view` que realiza un LEFT JOIN entre
        las tablas `tasks` y `employee`. Se usa para consultas combinadas.

        Raises:
            DatabaseError: Si ocurre un error al crear la vista.

        Example:
            >>> manager.create_view()
        """
        script = """
DROP VIEW IF EXISTS employee_tasks_view;
CREATE VIEW employee_tasks_view AS
SELECT
  t.id AS task_id,
  e.id AS employee_id,
  e.name AS employee_name,
  t.description,
  t.status,
  t.start_time,
  t.finish_time
FROM tasks t
LEFT JOIN employee e ON e.id = t.employee_id;
"""
        try:
            self.db.executescript(script)
        except DatabaseError:
            raise

    @log_execution
    def get_combined_data(self) -> tuple:
        """Obtiene datos combinados de empleados y tareas.

        Retorna dos listas: una con todos los empleados y otra con todas
        las tareas (incluyendo el nombre del empleado asignado).

        Returns:
            tuple: Tupla (employees, tasks) donde:
                - employees: list[tuple] con (id, name, surname, country, email)
                - tasks: list[tuple] con (task_id, description, status, employee_name)

        Raises:
            DatabaseError: Si ocurre un error al recuperar los datos.

        Example:
            >>> employees, tasks = manager.get_combined_data()
            >>> for emp in employees:
            ...     print(emp)
            >>> for task in tasks:
            ...     print(task)
        """
        try:
            employees = self.employee.get_all()
            tasks = self.task.get_all_with_employee()
            return (employees, tasks)
        except DatabaseError:
            raise

    def close(self) -> None:
        """Cierra la conexión a la base de datos.

        Libera los recursos asignados. Debe llamarse antes de
        finalizar la aplicación.

        Example:
            >>> manager.close()
        """
        self.db.close()
