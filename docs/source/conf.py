project = 'S2E API Documentation'
copyright = '2026, S2E Authors'
author = 'Hermes Agent'
release = '0.1.2'

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinxcontrib.mermaid',
]

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}
source_suffix = {'.md': 'markdown', '.rst': 'restructuredtext'}
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
myst_enable_extensions = ['colon_fence', 'deflist']
html_static_path = []
pygments_style = 'sphinx'
