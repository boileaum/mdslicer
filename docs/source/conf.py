# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# Get the project version from the package
from mdslicer import __version__

project = "mdslicer"
copyright = "2024 Matthieu Boileau"
author = "Matthieu Boileau"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",  # Markdown support
    "sphinx.ext.autodoc",  # Include documentation from docstrings
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx_copybutton",  # Add copy buttons to code blocks
    "sphinx.ext.autosummary",  # Generate autodoc summaries
]

templates_path = ["_templates"]  # Directory containing template files
exclude_patterns = []  # Files or directories to ignore when looking for source files


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"  # Set the HTML theme

autodoc_default_options = {
    "members": True,  # Include all class and module members
    "show-inheritance": True,  # Include inherited members
    "member-order": "groupwise",  # Group members by type
    "private-members": False,  # Exclude private members
    "special-members": "__init__",  # Include the initialiser
}

autosummary_generate = True  # Turn on sphinx.ext.autosummary
add_module_names = False  # Remove module names from class/method signatures

# to display the Returns section in the same style as the Args section
napoleon_custom_sections = [("Returns", "params_style")]
