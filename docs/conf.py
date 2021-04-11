# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# pylint: skip-file


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import auraxium


# -- Project information -----------------------------------------------------

project = 'Auraxium'
copyright = '2020, Leonhard S.'
author = 'Leonhard S.'
version = auraxium.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']

# The documentation master file
master_doc = 'index'

# Add parentheses to any function and method references
add_function_parentheses = True

# Report broken links and other grievences
nitpicky = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# A project logo to display in the docs. Must be given as a path relative to
# the configuration directory (i.e. the one containing this file).
html_logo = '../assets/logo_rtd.png'

# Additional HTML theme settings, refer to the link below for options:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
html_theme_options = {
    'logo_only': True,
    'prev_next_buttons_location': 'both'
}


# -- Autodoc configuration ---------------------------------------------------

# Autodoc type hints do not like reimported entities, so its type hint parsing
# is disabled. The types are instead documented as part of the methods
# themselves.
autodoc_typehints = 'none'

# Control how autodoc members are sorted in the docs.
autodoc_member_order = 'groupwise'


# -- Intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'aiohttp': ('https://docs.aiohttp.org/en/stable/', None),
    'requests': ('https://docs.python-requests.org/en/master/', None),
    'yarl': ('https://yarl.readthedocs.io/en/latest/', None),
    'websockets': ('https://websockets.readthedocs.io/en/stable/', None)
}
