import json
import os
from django.conf import settings

path = os.path.dirname(__file__)
path = os.path.dirname(path)
path = os.path.join(path, "staticfiles")
path = os.path.join(path, "search")

os.chdir(path)

# Load the existing data
with open('search_index.json', 'r') as f:
    data = json.load(f)

# Find the "solverapp" item
for item in data['docs']:
    if item['title'] == 'solverapp':
        # Update its location
        item['location'] = '../../../solverapp'  # Replace with the actual URL
        item['text'] = 'Lost Vergelijking op en Laat deze zien'  # Replace with the actual description
        print("Item updated successfully")
        break
else:
    # If the "solverapp" item was not found, add a new one
    data['docs'].append({
        'location': '../../../solverapp',  # Replace with the actual URL
        'title': 'solverapp',
        'text': 'Lost Vergelijking op en Laat deze zien'  # Replace with the actual description
    })
    print("New item added successfully")

# Save the updated data
with open('search_index.json', 'w') as f:
    json.dump(data, f, indent=4)
    print("Data updated successfully")