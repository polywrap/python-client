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

# Generate necessary code for plugins
import os
import shutil
import subprocess

root_dir = os.path.join(os.path.dirname(__file__), "..", "..")

shutil.rmtree(os.path.join(root_dir, "docs", "source", "misc"), ignore_errors=True)
shutil.copytree(os.path.join(root_dir, "misc"), os.path.join(root_dir, "docs", "source", "misc"))

subprocess.check_call(["python", "scripts/extract_readme.py"], cwd=os.path.join(root_dir, "packages", "polywrap-client"))
shutil.copy2(os.path.join(root_dir, "packages", "polywrap-client", "README.rst"), os.path.join(root_dir, "docs", "source", "Quickstart.rst"))

sys_config_dir = os.path.join(root_dir, "packages", "config-bundles", "polywrap-sys-config-bundle")
subprocess.check_call(["yarn", "codegen"], cwd=sys_config_dir)

shutil.copy2(os.path.join(root_dir, "CONTRIBUTING.rst"), os.path.join(root_dir, "docs", "source", "CONTRIBUTING.rst"))
