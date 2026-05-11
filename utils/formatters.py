"""Utilidades de formato y presentación de datos.

Funciones auxiliares para formatear datos para mostrar.
"""

from utils.decorators import timer


@timer
def format_employee_name(name: str, surname: str) -> str:
    """Formatea nombre de empleado completo.

    Args:
        name (str): Nombre del empleado.
        surname (str): Apellido del empleado.

    Returns:
        str: Nombre formateado "Name Surname".

    Example:
        >>> format_employee_name("John", "Doe")
        'John Doe'
    """
    return f"{name} {surname}".strip()


@timer
def format_email(email: str) -> str:
    """Formatea email a minúsculas.

    Args:
        email (str): Email a formatear.

    Returns:
        str: Email en minúsculas.

    Example:
        >>> format_email("Test@EXAMPLE.COM")
        'test@example.com'
    """
    return email.lower().strip()


@timer
def format_date(date_str: str | None) -> str:
    """Formatea fecha para visualización.

    Args:
        date_str (str | None): Cadena de fecha o None.

    Returns:
        str: Fecha formateada o "(none)" si es None.

    Example:
        >>> format_date("2024-01-15")
        '2024-01-15'
        >>> format_date(None)
        '(none)'
    """
    return date_str if date_str else "(none)"


@timer
def truncate_text(text: str, max_length: int = 50) -> str:
    """Trunca texto a longitud máxima.

    Args:
        text (str): Texto a truncar.
        max_length (int): Longitud máxima. Por defecto 50.

    Returns:
        str: Texto truncado con "..." si excede longitud.

    Example:
        >>> truncate_text("Very long text", 10)
        'Very long...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
