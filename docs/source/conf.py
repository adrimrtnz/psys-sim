import os, sys

sys.path.insert(0, os.path.abspath('../../services/engine/src'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'P-System Membrane Computing Simulator'
copyright = '2025, Adrián Martínez'
author = 'Adrián Martínez'
release = '1.0.0'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Extrae docs de los docstrings
    'sphinx.ext.napoleon', # Soporte para docstrings de Google/NumPy
    'sphinx.ext.viewcode', # Enlaces al código fuente
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
