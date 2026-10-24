"""Turn the mkdocs-built oplosser page into the Django base template for the oplosser.

run_updates.bat first copies docs/static/mkdocs_build/oplosser/index.html to
oplosser/templates/oplosser/base.html and then runs this script, which:
- replaces the page content with a Django `{% block content %}`
- points the mkdocs css/js/images at Django's `{% static %}` files
- swaps MathJax 3 for MathJax 2, which the oplosser templates use
"""

from pathlib import Path

import regex as re
from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString, Tag

TEMPLATE_PATH = Path(__file__).parent / "templates" / "oplosser" / "base.html"

MATHJAX_2_URL = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

# mkdocs files that are served through Django's static files. The hashes in the material theme's
# file names change with every mkdocs-material version, so they're matched with a pattern.
STATIC_FILE_PATTERN = re.compile(
    r"^\.\./("
    r"assets/stylesheets/(main|palette)\.[0-9a-f]+\.min\.css"
    r"|assets/images/general/calculator-variant(-outline)?\.(ico|svg)"
    r"|stylesheets/(extra|bootstrap-forms)\.css"
    r")$"
)


def use_static_tag(soup: BeautifulSoup, tag: Tag, attribute: str) -> None:
    value = tag.get(attribute)
    if not isinstance(value, str):
        return

    if value == "../stylesheets/extra.css":
        bootstrap_link = soup.new_tag("link", rel="stylesheet", href="{% static 'stylesheets/bootstrap-forms.css' %}")
        tag.insert_after(bootstrap_link)

    if STATIC_FILE_PATTERN.match(value):
        tag[attribute] = "{% static '" + value.removeprefix("../") + "' %}"


def fix_scripts(soup: BeautifulSoup) -> None:
    # The oplosser uses the MathJax 2 API (MathJax.Hub.Typeset), so MathJax 3 from the mkdocs pages
    # must not be loaded as well: both define window.MathJax and break each other.
    # Plotly is loaded by equation_form.html itself, so it doesn't depend on this script.
    for script in soup.find_all("script"):
        src = script.get("src")
        if not isinstance(src, str):
            continue

        if src == "../javascripts/mathjax.js":
            script["src"] = MATHJAX_2_URL
        elif "mathjax@3" in src or "/mathjax/3" in src:
            script.decompose()


def use_title_block(soup: BeautifulSoup) -> None:
    for title in soup.find_all("span", class_="md-ellipsis"):
        text = title.string
        if not isinstance(text, NavigableString):
            continue
        if "{{title}}" in text:
            return
        if "Oplosser" in text:
            text.replace_with("{{title}}")
            return


def escape_copyright_sign(soup: BeautifulSoup) -> None:
    copyright_div = soup.find("div", class_="md-copyright__highlight")
    if not isinstance(copyright_div, Tag):
        return

    for string in list(copyright_div.descendants):
        if isinstance(string, NavigableString) and not isinstance(string, Comment) and "©" in string:
            string.replace_with(NavigableString(string.replace("©", "&copy;")))


def update_base_template(template_path: Path) -> None:
    soup = BeautifulSoup(template_path.read_text(encoding="utf-8"), "lxml")

    content = soup.find("article")
    if not isinstance(content, Tag):
        raise ValueError(f"No <article> found in {template_path}; was the mkdocs page copied?")
    content.clear()
    content.insert(0, "{% block content %}{% endblock %}")

    for link in soup.find_all("link"):
        use_static_tag(soup, link, "href")

    for img in soup.find_all("img"):
        use_static_tag(soup, img, "src")

    fix_scripts(soup)
    use_title_block(soup)
    escape_copyright_sign(soup)

    html_tag = soup.find("html")
    if isinstance(html_tag, Tag):
        html_tag.insert(0, "{% load static %}")

    html_document = str(soup.prettify()).replace("&amp;copy;", "&copy;")
    template_path.write_text(html_document, encoding="utf-8")


if __name__ == "__main__":
    update_base_template(TEMPLATE_PATH)
