"""Validador de direcciones de correo electrónico.

Valida el formato de emails según expresiones regulares.
"""

import re
from validators.exceptions import EmailValidatorError


class EmailValidator:
    """Validador de emails.

    Realiza validación de formato de correo electrónico.

    Example:
        >>> validator = EmailValidator()
        >>> validator.validate('user@example.com')
        True
    """

    def __init__(self):
        """Inicializa validador con patrón regex."""
        self.pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    def validate(self, email: str) -> bool:
        """Valida el formato de una dirección de correo.

        Args:
            email (str): Dirección de correo a validar.

        Returns:
            bool: True si el formato es válido, False en caso contrario.

        Example:
            >>> validator = EmailValidator()
            >>> validator.validate('test@example.com')
            True
            >>> validator.validate('invalid-email')
            False
        """
        return bool(re.match(self.pattern, email))

    def validate_strict(self, email: str) -> bool:
        """Valida email y lanza excepción si es inválido.

        Args:
            email (str): Dirección de correo a validar.

        Returns:
            bool: True si es válido.

        Raises:
            EmailValidatorError: Si el email es inválido.

        Example:
            >>> validator = EmailValidator()
            >>> validator.validate_strict('test@example.com')
            True
        """
        if not self.validate(email):
            raise EmailValidatorError(f"Invalid email format: {email}")
        return True


# Instancia global para compatibilidad con código anterior
_email_validator = EmailValidator()


def validate_email(email: str) -> bool:
    """Valida el formato de una dirección de correo.

    Función de compatibilidad con código anterior.

    Args:
        email (str): Dirección de correo a validar.

    Returns:
        bool: True si el formato es válido.

    Example:
        >>> validate_email('user@example.com')
        True
    """
    return _email_validator.validate(email)
