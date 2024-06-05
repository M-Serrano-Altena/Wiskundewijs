import json
import os
from django.conf import settings

def update_search_index():
    # Load the existing data
    with open('search_index.json', 'r') as f:
        data = json.load(f)

    # Find the "solverapp" item
    for item in data['docs']:
        if item['title'] == 'Vergelijking Oplosser':
            # Update its location
            item['location'] = '../oplosser'  # Replace with the actual URL
            item['text'] = 'Lost een vergelijking op en plot de twee functies aan beide kanten'  # Replace with the actual description
            print("Item updated successfully")
            break
    else:
        # If the "solverapp" item was not found, add a new one
        data['docs'].append({
            'location': '../oplosser',  # Replace with the actual URL
            'title': 'Vergelijking Oplosser',
            'text': 'Lost een vergelijking op en plot de twee functies aan beide kanten'  # Replace with the actual description
        })
        print("New item added successfully")

    # Save the updated data
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

