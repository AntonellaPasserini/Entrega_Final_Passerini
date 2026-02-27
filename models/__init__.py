"""Paquete de modelos de datos.

Contiene los modelos, excepciones y utilidades para la gestión de la base de datos.
Exporta las clases principales para facilitar las importaciones.
"""

from models.exceptions import DatabaseError, ValidationError
from models.database import DatabaseConnection
from models.employee_model import EmployeeModel
from models.task_model import TaskModel
from models.backlog_model import BacklogModel
from models.database_manager import DatabaseManager

__all__ = [
    'DatabaseError',
    'ValidationError',
    'DatabaseConnection',
    'EmployeeModel',
    'TaskModel',
    'BacklogModel',
    'DatabaseManager',
]
