"""mkdocs hook: replace {year} in the copyright line with the year the site is built.

The year then updates whenever the site is rebuilt, but stays at the last update
if the site isn't touched anymore.
"""

from datetime import date

from mkdocs.config.defaults import MkDocsConfig


def on_config(config: MkDocsConfig) -> MkDocsConfig:
    if config.copyright:
        config.copyright = config.copyright.replace("{year}", str(date.today().year))
    return config
