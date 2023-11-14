"""
paginators.py: File, containing paginators for a project.
"""


from typing import ClassVar
from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    """
    CustomCursorPagination: Customer pagination class for a full project.

    Args:
        CursorPagination (CursorPagination): Build-in superclass for a CustomCursorPagination.
    """

    page_size: ClassVar[int] = 50
    max_page_size: ClassVar[int] = 200
    page_size_query_param: ClassVar[str] = 'page_size'
    page_size_query_description: ClassVar[str] = 'Number of results to return per page.'
    cursor_query_param: ClassVar[str] = 'cursor'
    cursor_query_description: ClassVar[str] = 'The pagination cursor value.'
    invalid_cursor_message: ClassVar[str] = 'Invalid cursor value.'
