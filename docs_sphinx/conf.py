# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PorosData-Processor'
copyright = '2026, Kivent YE'
author = 'Kivent YE'
release = '0.2.2'
version = '0.2.2'

# Add project description
description = 'A specialized text cleaning pipeline for AI for Science applications'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser',  # Enable MyST (Markdown) parser
]

# MyST Parser configuration
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "html_admonition",
    "html_image",
    # "linkify",  # Disabled: requires linkify-it-py dependency
    "replacements",
    "smartquotes",
    "strikethrough",
    "tasklist",
]

myst_heading_anchors = 3

# Source file suffixes - let MyST handle .md files automatically
# source_suffix = ['.rst', '.md']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add custom CSS files
html_css_files = [
    'custom.css',
]

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
