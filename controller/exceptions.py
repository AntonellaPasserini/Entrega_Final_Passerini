"""Excepciones personalizadas para el controlador.

Define errores específicos del flujo de control.
"""


class ControllerError(Exception):
    """Error base del controlador.

    Excepción general para errores de control.

    Example:
        >>> raise ControllerError("Control flow error")
    """

    def __init__(self, message: str):
        """Inicializa excepción.

        Args:
            message (str): Descripción del error.
        """
        self.message = message
        super().__init__(self.message)
