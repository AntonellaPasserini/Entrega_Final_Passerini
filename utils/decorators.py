"""Decoradores reutilizables para la aplicación.

Proporciona decoradores para logging, manejo de errores, validación,
timing y caching de funciones.
"""

import functools
import time
from typing import Any, Callable, TypeVar, cast
from utils.logging import log_event, log_error, log_success

F = TypeVar('F', bound=Callable[..., Any])


def log_execution(func: F) -> F:
    """Registra la ejecución de una función (entrada, salida y errores).

    Decora una función para registrar:
    - Cuando se llama (con parámetros)
    - Resultado exitoso
    - Errores ocurridos

    Args:
        func: Función a decorar.

    Returns:
        Función decorada con logging.

    Example:
        >>> @log_execution
        ... def add_employee(name: str, email: str) -> int:
        ...     return 1
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = func.__name__
        params_str = f"args={args[:2] if len(args) > 2 else args}, kwargs={kwargs}"
        print(log_event("INFO", f"Calling {func_name}", {"params": params_str}))
        
        try:
            result = func(*args, **kwargs)
            print(log_success(f"{func_name} completed", {"result": str(result)[:50]}))
            return result
        except Exception as exc:
            print(log_error(f"Error in {func_name}", exc))
            raise
    
    return cast(F, wrapper)


def handle_database_errors(func: F) -> F:
    """Maneja errores de base de datos automáticamente.

    Decora una función para capturar excepciones de base de datos
    y loguearlas de forma consistente.

    Args:
        func: Función a decorar.

    Returns:
        Función decorada con manejo de errores.

    Example:
        >>> @handle_database_errors
        ... def get_employee(emp_id: int):
        ...     pass
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            func_name = func.__name__
            print(log_error(f"Database error in {func_name}", exc))
            raise
    
    return cast(F, wrapper)


def timer(func: F) -> F:
    """Mide y registra el tiempo de ejecución de una función.

    Útil para identificar "cuellos de botella" en operaciones
    de base de datos y lógica de negocio.

    Args:
        func: Función a medir.

    Returns:
        Función decorada con timing.

    Example:
        >>> @timer
        ... def slow_query():
        ...     time.sleep(1)
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = func.__name__
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            print(log_event(
                "INFO",
                f"{func_name} executed",
                {"duration_ms": f"{elapsed*1000:.2f}"}
            ))
            return result
        except Exception as exc:
            elapsed = time.time() - start_time
            print(log_error(
                f"{func_name} failed after {elapsed*1000:.2f}ms",
                exc
            ))
            raise
    
    return cast(F, wrapper)


def cache_result(func: F) -> F:
    """Cachea el resultado de una función (simple).

    Útil para consultas de solo lectura que no cambian frecuentemente.
    Almacena el resultado en un diccionario keyed por parámetros.

    NOTA: No es thread-safe. Para aplicaciones concurrentes,
    usar bibliotecas especializadas.

    Args:
        func: Función a cachear.

    Returns:
        Función decorada con caching.

    Example:
        >>> @cache_result
        ... def get_all_employees():
        ...     return [...]  # operación costosa
    """
    cache: dict = {}
    
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Crear key basada en parámetros
        cache_key = (args, tuple(sorted(kwargs.items())))
        
        if cache_key in cache:
            print(log_event("INFO", f"{func.__name__} (cached)", {}))
            return cache[cache_key]
        
        result = func(*args, **kwargs)
        cache[cache_key] = result
        return result
    
    # Exponer método para limpiar cache
    wrapper.clear_cache = lambda: cache.clear()  # type: ignore
    
    return cast(F, wrapper)


def validate_not_none(*arg_names: str) -> Callable[[F], F]:
    """Valida que ciertos parámetros no sean None.

    Decora una función para verificar que parámetros específicos
    no tengan valor None antes de ejecutar.

    Args:
        *arg_names: Nombres de parámetros a validar (en orden).

    Returns:
        Decorador que valida parámetros no-None.

    Example:
        >>> @validate_not_none('emp_id', 'description')
        ... def add_task(emp_id: int, description: str):
        ...     pass
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_code = func.__code__
            var_names = func_code.co_varnames[:func_code.co_argcount]
            
            for arg_name in arg_names:
                if arg_name in var_names:
                    arg_index = var_names.index(arg_name)
                    if arg_index < len(args):
                        if args[arg_index] is None:
                            raise ValueError(f"Parameter '{arg_name}' cannot be None")
                    elif arg_name in kwargs and kwargs[arg_name] is None:
                        raise ValueError(f"Parameter '{arg_name}' cannot be None")
            
            return func(*args, **kwargs)
        
        return cast(F, wrapper)
    
    return decorator


def require_db_connection(func: F) -> F:
    """Valida que la conexión a base de datos esté activa.

    Decora métodos de modelos que requieren una conexión
    válida a la base de datos.

    Args:
        func: Función a decorar.

    Returns:
        Función decorada con validación de conexión.

    Example:
        >>> class EmployeeModel:
        ...     @require_db_connection
        ...     def get_all(self):
        ...         pass
    """
    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        # Verificar que el objeto tenga atributo 'db' y que sea válido
        if not hasattr(self, 'db'):
            raise RuntimeError(f"{func.__name__}: No database connection available")
        
        if self.db is None:
            raise RuntimeError(f"{func.__name__}: Database connection is None")
        
        # Verificar que la conexión tenga un cursor activo
        if not hasattr(self.db, 'cur') or self.db.cur is None:
            raise RuntimeError(f"{func.__name__}: Database cursor is not initialized")
        
        return func(self, *args, **kwargs)
    
    return cast(F, wrapper)


def deprecation_warning(message: str = "") -> Callable[[F], F]:
    """Marca una función como deprecada y registra advertencias.

    Decora una función para advertir que está deprecada antes
    de ejecutarla.

    Args:
        message: Mensaje adicional sobre la deprecación.

    Returns:
        Decorador que registra advertencias.

    Example:
        >>> @deprecation_warning("Use new_method instead")
        ... def old_method():
        ...     pass
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warning_msg = f"{func.__name__} is deprecated"
            if message:
                warning_msg += f": {message}"
            print(log_event("WARNING", warning_msg, {}))
            return func(*args, **kwargs)
        
        return cast(F, wrapper)
    
    return decorator
