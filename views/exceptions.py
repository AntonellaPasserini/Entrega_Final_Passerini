"""Excepciones personalizadas para la interfaz gráfica.

Define la jerarquía de excepciones para errores de UI y formularios.
"""


class UIError(Exception):
    """Error genérico relacionado con la interfaz gráfica.

    Se lanza cuando ocurren problemas en la renderización, eventos
    o gestión de ventanas.

    Attributes:
        message (str): Descripción detallada del error.
    """

    def __init__(self, message: str):
        """Inicializa la excepción de UI.

        Args:
            message (str): Descripción del error.
        """
        self.message = message
        super().__init__(self.message)


class FormError(Exception):
    """Error relacionado con validación o procesamiento de formularios.

    Se lanza cuando los datos del formulario no son válidos o
    ocurre un error al procesar el envío.

    Attributes:
        message (str): Descripción detallada del error.
    """

    def __init__(self, message: str):
        """Inicializa la excepción de formulario.

        Args:
            message (str): Descripción del error.
        """
        self.message = message
        super().__init__(self.message)
