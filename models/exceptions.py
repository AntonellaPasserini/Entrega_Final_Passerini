"""Excepciones personalizadas para la gestión de errores.

Define la jerarquía de excepciones para capturar errores de base de datos
y validación de datos de forma centralizada.
"""


class DatabaseError(Exception):
    """Error genérico relacionado con la base de datos.

    Se lanza cuando ocurren problemas de conexión, ejecución de consultas SQL
    o transacciones con la base de datos.

    Attributes:
        message (str): Descripción detallada del error.
    """

    def __init__(self, message: str):
        """Inicializa la excepción de base de datos.

        Args:
            message (str): Descripción del error.
        """
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """Error de validación de datos de entrada.

    Se lanza cuando los datos proporcionados no cumplen con los requisitos
    de validación (formato email, valores numéricos, campos obligatorios, etc.).

    Attributes:
        message (str): Descripción detallada del error de validación.
    """

    def __init__(self, message: str):
        """Inicializa la excepción de validación.

        Args:
            message (str): Descripción del error de validación.
        """
        self.message = message
        super().__init__(self.message)
