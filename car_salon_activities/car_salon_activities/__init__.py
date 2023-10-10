"""
__init__.py: File, that provides that celery application "app" will be created.
In fact, when python runs a program it needs to perform .py files to create objects.
If we use @shared_task (not @app.task) decorator then we will never import celery.py file.
If we will never import celery.py file then it will never perform and "app" won't be created.
Because of that, we import "app" here, because __init__ files perform always to init package.
"""


from .celery import app as celery_app


__all__: list = [
    'celery_app',
]
