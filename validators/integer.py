"""Validador de números enteros.

Valida que valores sean números enteros válidos.
"""

from validators.exceptions import IntegerValidatorError


class IntegerValidator:
    """Validador de números enteros.

    Valida que un valor sea un número entero.

    Example:
        >>> validator = IntegerValidator()
        >>> validator.validate('123')
        True
    """

    def validate(self, value: str) -> bool:
        """Verifica si una cadena representa un número entero.

        Args:
            value (str): Cadena a validar.

        Returns:
            bool: True si la cadena es un entero positivo, False en caso contrario.

        Example:
            >>> validator = IntegerValidator()
            >>> validator.validate('123')
            True
            >>> validator.validate('abc')
            False
        """
        return value.isdigit()

    def validate_strict(self, value: str) -> bool:
        """Valida entero y lanza excepción si es inválido.

        Args:
            value (str): Cadena a validar.

        Returns:
            bool: True si es válido.

        Raises:
            IntegerValidatorError: Si no es un entero válido.

        Example:
            >>> validator = IntegerValidator()
            >>> validator.validate_strict('123')
            True
        """
        if not self.validate(value):
            raise IntegerValidatorError(f"Must be a valid integer: {value}")
        return True

    def validate_range(self, value: str, min_val: int = 0, max_val: int | None = None) -> bool:
        """Valida que un entero esté en un rango específico.

        Args:
            value (str): Cadena a validar.
            min_val (int): Valor mínimo (inclusive). Por defecto 0.
            max_val (int | None): Valor máximo (inclusive). None para sin límite.

        Returns:
            bool: True si está en rango.

        Example:
            >>> validator = IntegerValidator()
            >>> validator.validate_range('50', min_val=0, max_val=100)
            True
        """
        if not self.validate(value):
            return False
        num = int(value)
        if num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True


# Instancia global para compatibilidad
_int_validator = IntegerValidator()


def validate_int(value: str) -> bool:
    """Verifica si una cadena representa un número entero.

    Función de compatibilidad con código anterior.

    Args:
        value (str): Cadena a validar.

    Returns:
        bool: True si la cadena es un entero positivo.

    Example:
        >>> validate_int('123')
        True
    """
    return _int_validator.validate(value)
