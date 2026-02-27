"""Utilidades de logging y debugging.

Funciones auxiliares para logueo de eventos y debugging.
"""

from datetime import datetime
from typing import Any


def log_event(event_type: str, message: str, details: dict | None = None) -> str:
    """Registra un evento con timestamp.

    Args:
        event_type (str): Tipo de evento (INFO, ERROR, WARNING, etc).
        message (str): Mensaje del evento.
        details (dict | None): Detalles adicionales del evento.

    Returns:
        str: Línea de log formateada.

    Example:
        >>> log_event("INFO", "Employee added", {"emp_id": 1})
        '2024-01-15 10:30:45 | INFO | Employee added | emp_id: 1'
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} | {event_type} | {message}"
    
    if details:
        details_str = " | ".join([f"{k}: {v}" for k, v in details.items()])
        log_line += f" | {details_str}"
    
    return log_line


def log_error(message: str, exception: Exception | None = None) -> str:
    """Registra un error con información de excepción.

    Args:
        message (str): Mensaje de error.
        exception (Exception | None): Excepción asociada (opcional).

    Returns:
        str: Línea de log de error formateada.

    Example:
        >>> try:
        ...     x = 1/0
        ... except Exception as e:
        ...     log_error("Division error", e)
    """
    log_line = log_event("ERROR", message)
    
    if exception:
        exc_info = f" | Exception: {type(exception).__name__}: {str(exception)}"
        log_line += exc_info
    
    return log_line


def log_success(message: str, data: Any | None = None) -> str:
    """Registra una operación exitosa.

    Args:
        message (str): Mensaje de éxito.
        data (Any | None): Datos retornados (opcional).

    Returns:
        str: Línea de log de éxito formateada.

    Example:
        >>> log_success("Employee created", {"emp_id": 1})
    """
    log_line = log_event("SUCCESS", message)
    
    if data is not None:
        log_line += f" | Result: {data}"
    
    return log_line
