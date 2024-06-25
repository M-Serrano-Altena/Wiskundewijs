import json
import os
from django.conf import settings

def update_search_index():
    # Load the existing data
    with open('search_index.json', 'r') as f:
        data = json.load(f)

    for item in data['docs']:
        if item['title'] == 'Vergelijking Oplosser':
            item['location'] = '../oplosser'
            item['text'] = 'Lost een vergelijking op en plot de twee functies aan beide kanten' 
            print("Item updated successfully")
            break
    else:
        data['docs'].append({
            'location': '../oplosser', 
            'title': 'Vergelijking Oplosser',
            'text': 'Lost een vergelijking op en plot de twee functies aan beide kanten'
        })
        print("New item added successfully")

    with open('search_index.json', 'w') as f:
        json.dump(data, f, indent=4)
        print("Data updated successfully")
        print()

base_path = os.path.dirname(__file__)
base_path = os.path.dirname(base_path)
path = os.path.join(base_path, "staticfiles", "search")

os.chdir(path)

update_search_index()

path = os.path.join(base_path, "docs", "static", "mkdocs_build", "search")
os.chdir(path)

update_search_index()

