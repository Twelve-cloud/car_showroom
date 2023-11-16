"""
schema.py: File, containing auth schema for a project.
"""


from typing import TYPE_CHECKING, Final
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from drf_spectacular.extensions import OpenApiAuthenticationExtension


if TYPE_CHECKING:
    from drf_spectacular.openapi import AutoSchema


class JWTTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    """
    JWTTokenAuthenticationScheme: Schema for a customer auth class.

    Args:
        OpenApiAuthenticationExtension (_type_): Base superclass.
    """

    target_class: None | str | type[object] = 'jauth.authentication.JWTAuthentication'
    name: Final[str | list[str]] = 'JWT_auth'

    def get_security_definition(self, auto_schema: 'AutoSchema') -> dict | list[dict]:
        return build_bearer_security_scheme_object(
            header_name='AUTHORIZATION',
            token_prefix='Bearer',
            bearer_format='JWT',
        )
