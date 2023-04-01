# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Import projects ---------------------------------------------------------


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'polywrap-client'
copyright = '2023, Niraj <niraj@polywrap.io>, Cesar <cesar@polywrap.io>'
author = 'Niraj <niraj@polywrap.io>, Cesar <cesar@polywrap.io>'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  "sphinx.ext.autodoc",
  "sphinx.ext.napoleon",
  "sphinx.ext.autosummary",
  "sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
