"""Paquete utils - Utilidades auxiliares de la aplicación.

Contiene funciones auxiliares para formateo, logging y operaciones generales.
"""

from utils.formatters import format_employee_name, format_email, format_date, truncate_text
from utils.logging import log_event, log_error, log_success
from utils.helpers import safe_get, is_valid_id, batch_list, flatten_list

__all__ = [
    # Formatters
    "format_employee_name",
    "format_email",
    "format_date",
    "truncate_text",
    # Logging
    "log_event",
    "log_error",
    "log_success",
    # Helpers
    "safe_get",
    "is_valid_id",
    "batch_list",
    "flatten_list",
]
