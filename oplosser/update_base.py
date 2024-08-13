import os
from bs4 import BeautifulSoup

def prettify_html(file_path):
    with open(file_path, 'r+') as file:
        soup = BeautifulSoup(file, 'lxml')

        file.seek(0)
        file.write(soup.prettify())
        file.truncate()

# prettify_html('templates/oplosser/test_base.html')


def update_base_template(file_path, files=None):
    def add_static_tag(tag, attribute):
        if tag.get(attribute) == r'../stylesheets/extra.css':
            new_link = soup.new_tag('link')
            new_link['rel'] = 'stylesheet'
            new_link['href'] = r"{% static 'stylesheets/bootstrap-forms.css' %}"
            tag.insert_after(new_link)

        if tag.get(attribute) in files:
            file = tag.get(attribute).split('../')[-1]
            tag[attribute] = r"{% static '" + file + r"' %}"

        return tag


    # Read the base.html template
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'lxml')

    content = soup.find('article')
    content.clear()
    content.insert(0, r"{% block content %}{% endblock %}")

    for link in soup.find_all('link'):
        link = add_static_tag(link, 'href')

    for img in soup.find_all('img'):
        img = add_static_tag(img, 'src')

    for script in soup.find_all('script'):
        if script.get("src") == r'../javascripts/mathjax.js':
            script["src"] = r"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

        elif script.get("src") == r"https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js":
            script["src"] = r"https://cdn.plot.ly/plotly-2.33.0.min.js"
            script["charset"] = r"utf-8"

    html_tag = soup.find('html')
    html_tag.insert(0, r"{% load static %}")

    for title in soup.find_all('span', class_="md-ellipsis"):
        if r"{{title}}" in title.string:
            break

        elif "Oplosser" in title.string:
            title.string.replace_with(r"{{title}}")
            break

    copy = soup.find('div', class_="md-copyright__highlight")
    strings = [string for string in copy.strings]
    for string in strings:
        if "©" in string:
            new_string = string.replace("©", r"&copy;")
            string.replace_with(new_string)

    html_document = soup.prettify()
    html_document = str(html_document).replace('&amp;copy;', '&copy;')

    # print(html_document)

    # Write the updated base.html template
    with open(file_path, 'w') as file:
        file.write(html_document)



oplosser_path = os.path.dirname(__file__)
os.chdir(oplosser_path)

files = [r'../assets/images/general/calculator-variant.ico', r'../assets/stylesheets/main.fad675c6.min.css', r'../assets/stylesheets/palette.356b1318.min.css', r'../stylesheets/extra.css', r'../stylesheets/bootstrap-forms.css', r'../assets/images/general/calculator-variant-outline.svg', r'../assets/javascripts/bundle.6c14ae12.min.js']
update_base_template(file_path='templates/oplosser/base.html', files=files)

base_path = os.path.dirname(oplosser_path)
os.chdir(base_path)