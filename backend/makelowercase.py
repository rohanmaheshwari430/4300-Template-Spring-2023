import json

# Open the data.json file and load its contents into a dictionary
with open('data.json', 'r') as f:
    data = json.load(f)

# Convert all keys in the "lyrics" attribute to lowercase
if 'lyrics' in data:
    lyrics_dict = data['lyrics']
    lyrics_dict = {k.lower(): v for k, v in lyrics_dict.items()}
    data['lyrics'] = lyrics_dict

# Save the updated data back to the data.json file
with open('data.json', 'w') as f:
    json.dump(data, f)