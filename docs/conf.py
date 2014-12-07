# -*- coding: utf-8 -*-
#
# Tarbell documentation build configuration file, created by
# sphinx-quickstart on Fri Sep 27 12:40:21 2013.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
#import sphinx_rtd_theme

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Tarbell'
copyright = u'2013, Chicago Tribune News Applications Team and David Eads'

# The short X.Y version.
version = '0.9'

# The full version, including alpha/beta/rc tags.
release = '0.9-beta5'

exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = "sphinx_rtd_theme"

#html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = False

# Output file base name for HTML help builder.
htmlhelp_basename = 'Tarbelldoc'

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'tarbell', u'Tarbell Documentation',
     [u'News Apps and David Eads'], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'Tarbell', u'Tarbell Documentation',
   u'News Apps and David Eads', 'Tarbell', 'A very simple publishing tool.',
   'Miscellaneous'),
]
