"""Utilidades diversas de la aplicación.

Funciones auxiliares generales reutilizables.
"""

from typing import Any
from utils.decorators import timer


@timer
def safe_get(obj: dict, key: str, default: Any = None) -> Any:
    """Obtiene valor de diccionario de forma segura.

    Args:
        obj (dict): Diccionario de donde obtener valor.
        key (str): Clave a buscar.
        default (Any): Valor por defecto si no existe.

    Returns:
        Any: Valor del diccionario o default.

    Example:
        >>> data = {"name": "John"}
        >>> safe_get(data, "name")
        'John'
        >>> safe_get(data, "age", 0)
        0
    """
    return obj.get(key, default) if obj else default


@timer
def is_valid_id(value: Any) -> bool:
    """Verifica si un valor es un ID válido (entero positivo).

    Args:
        value (Any): Valor a verificar.

    Returns:
        bool: True si es un ID válido.

    Example:
        >>> is_valid_id(1)
        True
        >>> is_valid_id(-1)
        False
    """
    try:
        num = int(value)
        return num > 0
    except (ValueError, TypeError):
        return False


@timer
def batch_list(items: list, batch_size: int) -> list[list]:
    """Divide una lista en lotes.

    Args:
        items (list): Lista a dividir.
        batch_size (int): Tamaño de cada lote.

    Returns:
        list[list]: Lista de lotes.

    Example:
        >>> batch_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


@timer
def flatten_list(nested_list: list) -> list:
    """Aplana una lista anidada.

    Args:
        nested_list (list): Lista anidada a aplanar.

    Returns:
        list: Lista aplada.

    Example:
        >>> flatten_list([[1, 2], [3, [4, 5]]])
        [1, 2, 3, 4, 5]
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result
