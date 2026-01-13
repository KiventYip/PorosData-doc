# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
from urllib.parse import urlparse

def validate_url(url: str, allowed_domains: list = None) -> bool:
    """
    Validate URL for security (prevent open redirect attacks).

    Args:
        url: URL to validate
        allowed_domains: List of allowed domains, defaults to readthedocs.io

    Returns:
        bool: True if URL is safe
    """
    if not url:
        return True  # Empty URLs are allowed

    if allowed_domains is None:
        allowed_domains = ['readthedocs.io', 'readthedocs.com']

    try:
        parsed = urlparse(url)
        if not parsed.scheme in ['http', 'https']:
            return False
        if not any(domain in parsed.netloc for domain in allowed_domains):
            return False
        return True
    except Exception:
        return False

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PorosData'
copyright = '2026, Kivent YE'
author = 'Kivent YE'
release = '0.2.2'
version = '0.2.2'

# Add project description
description = 'A comprehensive scientific data processing suite for AI for Science applications'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Core Sphinx extensions
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',

    # MyST Parser for Markdown support
    'myst_parser',

    # Documentation enhancements
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',

    # Development extensions (conditionally loaded)
    # 'sphinx.ext.autodoc',  # Enable only if API docs are generated
    # 'sphinx.ext.doctest',  # Enable only for testing
    # 'sphinx.ext.coverage', # Enable only for coverage reports
    # 'sphinx.ext.imgmath',  # Enable only if math rendering needed
    # 'sphinx.ext.ifconfig', # Enable only if conditional content needed
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

# Enhanced exclude patterns for security and cleanliness
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    # Security: Exclude common sensitive files
    '.env',
    '.env.*',
    '*.key',
    '*.pem',
    'secrets.*',
    'config.local.*',
    # Development artifacts
    '__pycache__',
    '*.pyc',
    '.pytest_cache',
    '.coverage',
    'htmlcov',
    # IDE and editor files
    '.vscode',
    '.idea',
    '*.swp',
    '*.swo',
    # OS generated files
    '.DS_Store',
    'Thumbs.db',
    'desktop.ini',
]

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add custom CSS files
html_css_files = [
    'custom.css',
]

# Theme options for RTD theme - optimized for PorosData ecosystem
html_theme_options = {
    # Navigation depth for cleaner sidebar
    'navigation_depth': 2,

    # Hide view source link for cleaner appearance
    'display_version': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,

    # Enhanced navigation settings - use titles_only to prevent long sidebar descriptions
    'collapse_navigation': True,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': True,

    # Footer customization
    'canonical_url': 'https://porosdata-doc.readthedocs.io/en/latest/',
    'analytics_id': '',  # Add Google Analytics ID if needed

    # Logo and branding (uncomment when logo is available)
    # 'logo_only': False,
    # 'logo': '_static/logo.png',
}

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

# -- Security and configuration validation ----------------------------------
# Validate critical configuration on import

def validate_configuration():
    """Validate configuration for security and correctness."""
    errors = []

    # Validate canonical URL
    canonical_url = html_theme_options.get('canonical_url', '')
    if canonical_url and not validate_url(canonical_url):
        errors.append(f"Invalid canonical URL: {canonical_url}")

    # Validate project information
    if not project or len(project.strip()) == 0:
        errors.append("Project name is required")

    if not author or len(author.strip()) == 0:
        errors.append("Author is required")

    # Check for potentially dangerous extensions
    dangerous_extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest']
    active_dangerous = [ext for ext in extensions if ext in dangerous_extensions]
    if active_dangerous:
        print(f"Warning: Potentially dangerous extensions enabled: {active_dangerous}")

    if errors:
        raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

    print("Configuration validation passed.")

# Run validation
validate_configuration()
