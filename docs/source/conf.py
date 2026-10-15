# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PandoraDocs'
copyright = '2026, Pandora Developers'
author = 'Pandora Development Team'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.extlinks',
]

templates_path = ['_templates']
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "work_items/template.rst",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

html_theme = 'sphinx_rtd_theme'
html_logo = '../../static/pandora_logo_square_bw.png'

html_theme_options = {
    'logo_only': True,
    'display_version': True,
}

# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- Options for extlinks extension -------------------------------------------
extlinks = {
    'pr': ('https://github.com/PandoraPFA/LArContent/pull/%s', 'PR #%s'),
    'tag': ('https://github.com/PandoraPFA/LArContent/tree/%s', 'LArContent %s'),
    'core': ('https://github.com/PandoraPFA/LArContent/blob/master/%s', '%s')
}
