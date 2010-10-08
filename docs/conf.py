# -*- coding: utf-8 -*-

import os.path
import sys

# Add module path to system path so autodoc can find it
sys.path.append(os.path.normpath('../'))

# Add path to inkex
sys.path.append('/usr/share/inkscape/extensions')

# Extensions in use
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.pngmath',
             'sphinxtogithub']
autoclass_content = 'both'
pngmath_dvipng_args = ['-gamma 1.5', '-D 100']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'inkscape-pybounds'
copyright = u'2010, Blair Bonnett'

# Version (x.y) and release (with alpha/beta etc.)
from bounds import version
release = version

# Documents not to include
unused_docs = []

# Directories not to search
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme_path = ['theme']
html_theme = 'boundsdocs'

# The name for this set of Sphinx documents.
html_title = 'inkscape-pybounds %s' % version

# Format for timestamp.
html_last_updated_fmt = '%b %d, %Y'

# Output file base name for HTML help builder.
htmlhelp_basename = 'inkscape-pyboundsdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
latex_paper_size = 'a4'

# The font size ('10pt', '11pt' or '12pt').
latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'inkscape-pybounds.tex', u'inkscape-pybounds Documentation',
   u'Blair Bonnett', 'manual'),
]

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'inkscape-pybounds', u'inkscape-pybounds Documentation',
     [u'Blair Bonnett'], 1)
]
