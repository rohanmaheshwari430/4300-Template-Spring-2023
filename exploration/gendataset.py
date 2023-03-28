from azapi import AZlyrics
import json


api = AZlyrics()
  
f = open('artists.json')
data = json.load(f)
f.close()

for artist in data:
    if not data[artist]:
        try:
            api.artist = artist
            songs = api.getSongs()

            for song in songs:
                api.getLyrics(url=songs[song]["url"], save=True, path=f"./lyrics/", sleep=5)
            data[artist]=True
            json_object = json.dumps(data, indent=4)
            with open("artists.json", "w") as outfile:
                outfile.write(json_object)
        except:
            print("failed to find " + artist)
            data[artist]=True



