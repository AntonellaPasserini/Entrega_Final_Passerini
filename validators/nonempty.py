"""Validador de campos no-vacíos.

Valida que campos requeridos contengan datos.
"""

from validators.exceptions import NonemptyValidatorError


class NonemptyValidator:
    """Validador de campos no-vacíos.

    Valida que un texto no esté vacío (solo espacios).

    Example:
        >>> validator = NonemptyValidator()
        >>> validator.validate('hello')
        True
    """

    def validate(self, text: str) -> bool:
        """Verifica que una cadena no esté vacía tras eliminar espacios.

        Args:
            text (str): Cadena a validar.

        Returns:
            bool: True si contiene carácteres no-espacios, False en caso contrario.

        Example:
            >>> validator = NonemptyValidator()
            >>> validator.validate('hello')
            True
            >>> validator.validate('   ')
            False
        """
        return bool(text and text.strip())

    def validate_strict(self, text: str, field_name: str = "Field") -> bool:
        """Valida no-vacío y lanza excepción si es inválido.

        Args:
            text (str): Cadena a validar.
            field_name (str): Nombre del campo para mensaje de error.

        Returns:
            bool: True si es válido.

        Raises:
            NonemptyValidatorError: Si el campo está vacío.

        Example:
            >>> validator = NonemptyValidator()
            >>> validator.validate_strict('hello', 'Name')
            True
        """
        if not self.validate(text):
            raise NonemptyValidatorError(f"{field_name} cannot be empty")
        return True

    def validate_min_length(self, text: str, min_length: int) -> bool:
        """Valida que un texto tenga longitud mínima.

        Args:
            text (str): Cadena a validar.
            min_length (int): Longitud mínima requerida.

        Returns:
            bool: True si cumple la longitud mínima.

        Example:
            >>> validator = NonemptyValidator()
            >>> validator.validate_min_length('hello', 3)
            True
        """
        if not self.validate(text):
            return False
        return len(text.strip()) >= min_length

    def validate_max_length(self, text: str, max_length: int) -> bool:
        """Valida que un texto no exceda longitud máxima.

        Args:
            text (str): Cadena a validar.
            max_length (int): Longitud máxima permitida.

        Returns:
            bool: True si no excede la longitud máxima.

        Example:
            >>> validator = NonemptyValidator()
            >>> validator.validate_max_length('hello', 10)
            True
        """
        if not self.validate(text):
            return False
        return len(text.strip()) <= max_length


# Instancia global para compatibilidad
_nonempty_validator = NonemptyValidator()


def validate_nonempty(text: str) -> bool:
    """Verifica que una cadena no esté vacía tras eliminar espacios.

    Función de compatibilidad con código anterior.

    Args:
        text (str): Cadena a validar.

    Returns:
        bool: True si contiene carácteres no-espacios.

    Example:
        >>> validate_nonempty('hello')
        True
    """
    return _nonempty_validator.validate(text)
