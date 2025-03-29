from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.static import serve
import os
import markdown
import re
from bs4 import BeautifulSoup
from textwrap import dedent


def serve_docs(request, path):
    if path == "oplosser":
        return redirect("oplosser")
    
    docs_path = os.path.join(settings.DOCS_DIR, path)

    if os.path.isdir(docs_path):
        path = os.path.join(path, 'index.html')

    path = os.path.join(settings.DOCS_DIR, path)
    relative_path = os.path.relpath(path, settings.DOCS_DIR)

    return serve(request, relative_path, settings.DOCS_DIR)


def serve_home(request):
    return serve_docs(request, 'index.html')

def load_external_html(request, path):
    path = path.replace(".md", "/index.html")
    if "index.html" not in path:
        path = path + "/index.html"

    file_path = os.path.join(settings.DOCS_DIR, path.replace(".md", "/index.html"))

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")

        # Extract content inside <article> for the page content
        main_content = soup.find("article")
        
        # Remove <h1> headers as needed (optional step)
        for h1 in main_content.find_all("h1"):
            h1.decompose()  # .decompose() removes the tag and its contents

        # Generate the TOC structure for this section
        toc_structure = generate_toc_structure(str(main_content))

        toc_html = generate_toc_html(toc_structure)

        # Combine the TOC and the content
        if main_content:
            html_content = str(main_content)
        else:
            html_content = "Error: Could not find main content."

        return JsonResponse({"content": html_content, "toc": toc_html})

    except FileNotFoundError:
        return JsonResponse({"error": "File not found"}, status=404)
    

def get_next_same_level_heading_index(soup, tag) -> int:
    all_headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    tag_index = all_headings.index(tag)
    for next_tag in all_headings[tag_index+1:]:
        if next_tag.name == tag.name:
            return all_headings.index(next_tag)
        
    return len(all_headings)

def generate_toc_structure(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Initialize an empty list for the TOC
    toc = []
    
    # Define a helper function to build TOC recursively
    def build_toc(soup, h_level=2, parent_tag_index=0):
        nav_items = []
        all_headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        parent_tag = all_headings[parent_tag_index]
        for i, tag in enumerate(all_headings[parent_tag_index:]):
            if tag.name != f"h{h_level}":
                continue
            
            current_tag_index = parent_tag_index + i

            # Skip this tag if it is not a direct child of the parent tag
            if current_tag_index > get_next_same_level_heading_index(soup, parent_tag):
                continue

            # Create a list item for the TOC entry
            toc_item = {
                'text': tag.get_text(strip=True),
                'id': tag.get('id', None),  # Use the ID attribute to create a link
                'children': build_toc(soup, h_level + 1, parent_tag_index=current_tag_index) if h_level < 6 else []
            }
            nav_items.append(toc_item)

        return nav_items
    
    toc = build_toc(soup)
    return toc

# generate Toc html based on the toc structure of a section (not chapter)
# actual merging of previous toc with this toc happens in load_sections.js
def generate_toc_html(toc_dict_structure):
    html = ""
    for item in toc_dict_structure:
        if item['id']:
            html += f'<li class="md-nav__item"><a href="#{item["id"]}" class="md-nav__link"><span class="md-ellipsis">{item["text"]}</span></a>'
        if item['children']:
            html += '<nav class="md-nav" aria-label="{item["text"]}">'
            html += '<ul class="md-nav__list">'
            html += generate_toc_html(item['children'])
            html += '</ul></nav>'
        html += '</li>'
    return html


def generate_html_toc_test(toc):
    hard_coded_toc = dedent("""
    <div class="md-sidebar md-sidebar--secondary" data-md-component="sidebar" data-md-type="toc">
    <div class="md-sidebar__scrollwrap">
        <div class="md-sidebar__inner">
        <nav class="md-nav md-nav--secondary" aria-label="Inhoudsopgave">
            <label class="md-nav__title" for="__toc">
            <span class="md-nav__icon md-icon"></span>
            Inhoudsopgave
            </label>
            <ul class="md-nav__list" data-md-component="toc" data-md-scrollfix>
            <li class="md-nav__item">
                <a href="#introductie-primitieven" class="md-nav__link">
                <span class="md-ellipsis">
                    Introductie Primitieven
                </span>
                </a>
                <nav class="md-nav" aria-label="Introductie Primitieven">
                <ul class="md-nav__list">
                    <li class="md-nav__item">
                    <a href="#tabel-met-veel-voorkomende-functies" class="md-nav__link">
                        <span class="md-ellipsis">
                        Tabel met veel voorkomende functies
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#regels" class="md-nav__link">
                        <span class="md-ellipsis">
                        Regels
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#voorbeelden" class="md-nav__link">
                        <span class="md-ellipsis">
                        Voorbeelden
                        </span>
                    </a>
                    </li>
                </ul>
                </nav>
            </li>
            <li class="md-nav__item">
                <a href="#introductie-integralen" class="md-nav__link">
                <span class="md-ellipsis">
                    Introductie Integralen
                </span>
                </a>
                <nav class="md-nav" aria-label="Introductie Integralen">
                <ul class="md-nav__list">
                    <li class="md-nav__item">
                    <a href="#oppervlakte-onder-een-grafiek" class="md-nav__link">
                        <span class="md-ellipsis">
                        Oppervlakte onder een grafiek
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#integralen-uitwerken" class="md-nav__link">
                        <span class="md-ellipsis">
                        Integralen Uitwerken
                        </span>
                    </a>
                    <nav class="md-nav" aria-label="Integralen Uitwerken">
                        <ul class="md-nav__list">
                        <li class="md-nav__item">
                            <a href="#algemene-vorm" class="md-nav__link">
                            <span class="md-ellipsis">
                                Algemene Vorm
                            </span>
                            </a>
                        </li>
                        </ul>
                    </nav>
                    </li>
                    <li class="md-nav__item">
                    <a href="#oppervlaktes-onder-de-x-as" class="md-nav__link">
                        <span class="md-ellipsis">
                        Oppervlaktes onder de x-as
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#deel-boven-en-deel-onder-de-x-as" class="md-nav__link">
                        <span class="md-ellipsis">
                        Deel boven en deel onder de x-as
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#voorbeelden_1" class="md-nav__link">
                        <span class="md-ellipsis">
                        Voorbeelden
                        </span>
                    </a>
                    </li>
                </ul>
                </nav>
            </li>
            <li class="md-nav__item">
                <a href="#oppervlakte-tussen-twee-grafieken" class="md-nav__link">
                <span class="md-ellipsis">
                    Oppervlakte tussen twee grafieken
                </span>
                </a>
                <nav class="md-nav" aria-label="Oppervlakte tussen twee grafieken">
                <ul class="md-nav__list">
                    <li class="md-nav__item">
                    <a href="#integralen-samenvoegen" class="md-nav__link">
                        <span class="md-ellipsis">
                        Integralen samenvoegen
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#algemene-integraal" class="md-nav__link">
                        <span class="md-ellipsis">
                        Algemene Integraal
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#voorbeelden_2" class="md-nav__link">
                        <span class="md-ellipsis">
                        Voorbeelden
                        </span>
                    </a>
                    </li>
                </ul>
                </nav>
            </li>
            <li class="md-nav__item">
                <a href="#oppervlakte-wentelen-om-de-x-as" class="md-nav__link">
                <span class="md-ellipsis">
                    Oppervlakte wentelen om de x-as
                </span>
                </a>
                <nav class="md-nav" aria-label="Oppervlakte wentelen om de x-as">
                <ul class="md-nav__list">
                    <li class="md-nav__item">
                    <a href="#algemene-integraal-wentelen-x-as" class="md-nav__link">
                        <span class="md-ellipsis">
                        Algemene Integraal Wentelen x-as
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#voorbeelden_3" class="md-nav__link">
                        <span class="md-ellipsis">
                        Voorbeelden
                        </span>
                    </a>
                    </li>
                </ul>
                </nav>
            </li>
            <li class="md-nav__item">
                <a href="#omwentelingslichaam-tussen-twee-grafieken" class="md-nav__link">
                <span class="md-ellipsis">
                    Omwentelingslichaam tussen twee grafieken
                </span>
                </a>
                <nav class="md-nav" aria-label="Omwentelingslichaam tussen twee grafieken">
                <ul class="md-nav__list">
                    <li class="md-nav__item">
                    <a href="#algemene-integraal-wentelen-x-as-tussen-grafieken" class="md-nav__link">
                        <span class="md-ellipsis">
                        Algemene Integraal Wentelen x-as tussen grafieken
                        </span>
                    </a>
                    </li>
                    <li class="md-nav__item">
                    <a href="#voorbeelden_4" class="md-nav__link">
                        <span class="md-ellipsis">
                        Voorbeelden
                        </span>
                    </a>
                    </li>
                </ul>
                </nav>
            </li>
            <li class="md-nav__item">
                <a href="#oppervlakte-wentelen-om-de-y-as" class="md-nav__link">
                <span class="md-ellipsis">
                    Oppervlakte wentelen om de y-as
                </span>
                </a>
            </li>
            </ul>
        </nav>
        </div>
    </div>
    </div>
    """.strip())

    return hard_coded_toc