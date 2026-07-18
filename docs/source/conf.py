# Configuration file for the Sphinx documentation builder.

# -- Project information
project = 'S2E API Documentation'
copyright = '2026, S2E Authors'
author = 'S2E Authors'
release = '0.1.2'
version = '0.1.2'

# -- General configuration
extensions = [
    'myst_parser',
    'sphinxcontrib.mermaid',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.duration',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
source_suffix = {'.md': 'markdown', '.rst': 'restructuredtext'}
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# MyST Parser extensions
myst_enable_extensions = ['colon_fence', 'deflist']

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}
html_static_path = []

# -- Options for EPUB output
epub_show_urls = 'footnote'

pygments_style = 'sphinx'
