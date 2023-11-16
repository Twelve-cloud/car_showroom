"""
dbrouters.py: File, containing routers for database operations.
"""


from typing import Any


class KubernetesRouter:
    """
    KubernetesRouter: A router to control all database operations on models in the all applications.
    """

    def db_for_read(self, model: Any, **hints: dict) -> str:
        """
        db_for_read: Sets database for reading.

        Args:
            model (Any): Model on which operation is performing.

        Returns:
            str: Database for reading.
        """

        return 'default'

    def db_for_write(self, model: Any, **hints: dict) -> str:
        """
        db_for_write: Sets database for writing.

        Args:
            model (Any): Model on which operation is performing.

        Returns:
            str: Database for writing.
        """

        return 'master'

    def allow_migrate(self, db: str, app_label: str, model_name: Any = None, **hints: dict) -> bool:
        """
        allow_migrate: Returns True if migration can be applied for a specific database.

        Args:
            db (str): Database.
            app_label (str): Label of an application.
            model_name (Any, optional): Model name. Defaults to None.

        Returns:
            bool: True if migrations can be applied otherwise False.
        """

        return db == 'master'
