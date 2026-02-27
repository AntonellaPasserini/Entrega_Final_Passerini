"""Excepciones personalizadas para validadores.

Define jerarquía de excepciones específicas para errores de validación.
"""


class ValidatorError(Exception):
    """Error base para validadores.

    Excepción general que representa un error en validación de datos.

    Example:
        >>> raise ValidatorError("Validation failed")
    """

    def __init__(self, message: str):
        """Inicializa excepción con mensaje.

        Args:
            message (str): Descripción del error.
        """
        self.message = message
        super().__init__(self.message)


class EmailValidatorError(ValidatorError):
    """Error específico de validación de email.

    Se lanza cuando el formato de email no es válido.

    Example:
        >>> raise EmailValidatorError("Email format invalid")
    """

    pass


class IntegerValidatorError(ValidatorError):
    """Error específico de validación de entero.

    Se lanza cuando un valor no es un entero válido.

    Example:
        >>> raise IntegerValidatorError("Must be an integer")
    """

    pass


class NonemptyValidatorError(ValidatorError):
    """Error específico de validación de no-vacío.

    Se lanza cuando un campo requerido está vacío.

    Example:
        >>> raise NonemptyValidatorError("Field cannot be empty")
    """

    pass
