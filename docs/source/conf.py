# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../../src/'))
print(sys.path)
#sys.path.insert(0, os.path.abspath('../../src/swagger_client'))

# -- Project information -----------------------------------------------------

project = 'pymzTab-m'
copyright = '2019, Nils Hoffmann'
author = 'Nils Hoffmann'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

#source_parsers = {
#    '.md': 'recommonmark.parser.CommonMarkParser',
#}

#source_suffix = ['.rst', '.md']

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinxcontrib.apidoc',
        'sphinx.ext.autodoc',
#	'recommonmark',
#        'sphinx_markdown_tables'
]

apidoc_module_dir = '../../src/'
apidoc_output_dir = 'api'
apidoc_exluded_paths = ['conftest']
apidoc_separate_modules = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']

master_doc = 'index'

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "lifs-tools", # Username
    "github_repo": "pymzTab-m", # Repo name
    "github_version": "master", # Version
    "conf_py_path": "/docs/source/", # Path in the checkout to the docs root
}

autoclass_content = "both"
