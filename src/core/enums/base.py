"""
base.py: File, containing base classes and metaclasses for enums for a project.
"""


from __future__ import annotations
from enum import EnumMeta
from typing import Any, ClassVar


class ReadOnlyChoicesDescriptor:
    """
    ReadOnlyChoicesDescriptor: Class descriptor, that provides special logic for attributes.
    """

    def __get__(self, instance: Any, owner: Any) -> list[tuple]:
        return [item.value for item in instance]

    def __set__(self, instance: Any, value: Any) -> None:
        raise AttributeError('Can not set value to read-only attribute')


class EnumMetaclass(EnumMeta):
    """
    EnumMetaclass: Metaclass for every enum in a project.

    Args:
        EnumMeta (_type_): Base metaclass for each Enum class and subclasses.
    """

    choices: ClassVar[ReadOnlyChoicesDescriptor] = ReadOnlyChoicesDescriptor()
