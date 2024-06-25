import xml.etree.ElementTree as ET
import gzip
import shutil
import os

def add_url_to_sitemap(sitemap_path, url):
    # Parse the existing sitemap.xml
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    # Check if the URL is already in the sitemap
    urls = [loc.text.strip() for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if url in urls:
        print(f"URL {url} already exists in sitemap.")
        return

    # Create a new <url> element
    new_url_elem = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    loc_elem = ET.SubElement(new_url_elem, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    loc_elem.text = url

    # Append the new <url> element to the root
    root.append(new_url_elem)

    # Write the modified sitemap.xml back to file
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)

    print(f"Added URL {url} to sitemap.")

    # If there's a sitemap.xml.gz, update it as well
    gz_file = sitemap_path + '.gz'
    if os.path.exists(gz_file):
        with gzip.open(gz_file, 'rb') as f_in:
            tree_gz = ET.parse(f_in)
            root_gz = tree_gz.getroot()

        # Check if the URL is already in the gzipped sitemap
        urls_gz = [loc.text.strip() for loc in root_gz.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        if url in urls_gz:
            print(f"URL {url} already exists in sitemap.xml.gz.")
            return

        # Create a new <url> element for the gzipped sitemap
        new_url_elem_gz = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        loc_elem_gz = ET.SubElement(new_url_elem_gz, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        loc_elem_gz.text = url

        # Append the new <url> element to the root of the gzipped sitemap
        root_gz.append(new_url_elem_gz)

        # Write the modified gzipped sitemap back to file
        with gzip.open(gz_file, 'wb') as f_out:
            tree_gz.write(f_out, encoding='utf-8', xml_declaration=True)

        print(f"Added URL {url} to sitemap.xml.gz.")

    else:
        print(f"No sitemap.xml.gz found. Skipping gzipped sitemap update.")


new_url = "https://wiskundewijs.com/oplosser/"

base_path = os.path.dirname(__file__)
base_path = os.path.dirname(base_path)


path = os.path.join(base_path, "docs", "static", "mkdocs_build")
os.chdir(path)
print()
print(f"In {os.getcwd()}:")
add_url_to_sitemap("sitemap.xml", new_url)

path = os.path.join(base_path, "staticfiles")
os.chdir(path)
print()
print(f"In {os.getcwd()}:")
add_url_to_sitemap("sitemap.xml", new_url)