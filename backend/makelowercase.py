import json

# def make_lowercase():
#   # Open the data.json file and load its contents into a dictionary
#   with open('data.json', 'r') as f:
#       data = json.load(f)

#   # Convert all keys in the "lyrics" attribute to lowercase
#   if 'lyrics' in data:
#       lyrics_dict = data['lyrics']
#       lyrics_dict = {k.lower(): v for k, v in lyrics_dict.items()}
#       data['lyrics'] = lyrics_dict

#   # Save the updated data back to the data.json file
#   with open('data.json', 'w') as f:
#       json.dump(data, f)

def remove_no_lyric_songs():
    lyrics = {
        "please": 1,
        "back": 1,
        "lyrics": 1,
        "released": 2,
        "yet": 1,
        "check": 1,
        "song": 2
      }
    with open('data.json', 'r') as f:
        data = json.load(f)
    songs = data['songs']
    for song in songs:
        if song['lyrics'].setdefault('please', 0) == 1 and song['lyrics'].setdefault('back', 0) == 1 and song['lyrics'].setdefault('lyrics', 0) == 1 and song['lyrics'].setdefault('released', 0) == 2 and song['lyrics'].setdefault('yet', 0) == 1 and song['lyrics'].setdefault('check', 0) == 1 and song['lyrics'].setdefault('song', 0) == 2:
            print(song['title'])
            songs.remove(song)
    data['songs'] = songs
    with open('data.json', 'w') as f:
        json.dump(data, f)

remove_no_lyric_songs()



