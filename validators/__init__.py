"""Paquete de validadores - Validación modular de datos.

Contiene validadores especializados para diferentes tipos de datos.
"""

from validators.email import EmailValidator, validate_email
from validators.integer import IntegerValidator, validate_int
from validators.nonempty import NonemptyValidator, validate_nonempty
from validators.exceptions import (
    ValidatorError,
    EmailValidatorError,
    IntegerValidatorError,
    NonemptyValidatorError,
)

__all__ = [
    # Clases
    "EmailValidator",
    "IntegerValidator",
    "NonemptyValidator",
    # Funciones de compatibilidad
    "validate_email",
    "validate_int",
    "validate_nonempty",
    # Excepciones
    "ValidatorError",
    "EmailValidatorError",
    "IntegerValidatorError",
    "NonemptyValidatorError",
]
