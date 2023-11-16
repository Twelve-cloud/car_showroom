from enum import Enum
from core.enums.base import EnumMetaclass


class Brands(Enum, metaclass=EnumMetaclass):
    """
    Brands: Enum, that represents brands.

    Args:
        Enum (_type_): Base Enum class from a standart library.
        metaclass (_type_, optional): Chosen metaclass. Defaults to EnumMetaclass.
    """

    AUDI: tuple[str, str] = 'audi', 'Audi'
    BMW: tuple[str, str] = 'bmw', 'BMW'
    TESLA: tuple[str, str] = 'tesla', 'Tesla'


class TransmissionTypes(Enum, metaclass=EnumMetaclass):
    """
    TransmissionTypes: Enum, that represents transmission types.

    Args:
        Enum (_type_): Base Enum class from a standart library.
        metaclass (_type_, optional): Chosen metaclass. Defaults to EnumMetaclass.
    """

    MANUAL: tuple[str, str] = 'manual', 'Manual'
    AUTO: tuple[str, str] = 'auto', 'Auto'
