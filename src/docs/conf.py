"""
conf.py: File, containing settings for a sphinx docs for a project.
"""


import os
import sys
import django


sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

project: str = 'Car Salon'
copyright: str = '2023, IS'
author: str = 'IS'
release: str = '0.1.0'
extensions: list[str] = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon']
exclude_patterns: list[str] = ['_build', 'Thumbs.db', '.DS_Store', '*test*']
html_theme: str = 'sphinx_material'
