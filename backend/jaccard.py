import json
import azapi 
from typing import List


API = azapi.AZlyrics('google', accuracy=0.5)

def find_sim(query_song_lyrics, query_song_name):
  f = open('data.json') # returns JSON object as a dictionary
  data = json.load(f)
  scores = []
  for song in data["songs"]:
        if song["title"] != query_song_name:
          song_lyrics = set(song["lyrics"].keys())
          intersection = song_lyrics.intersection(query_song_lyrics)
          union = song_lyrics.union(query_song_lyrics)
          if(len(union) == 0):
              scores.append((song["title"], 0))
          else:
            score = len(intersection) / len(union)
            scores.append((song["title"], score))
  scores.sort(key = lambda x: x[1],reverse=True)
  scores = scores[:10]
  final_list = []
  i = 0
  for (title,score) in scores:
      final_list.append(({'title': title ,'score': score}))
      i += 1
  return final_list



def get_song_lyrics(song_name):
  f = open('data.json')
  data = json.load(f)
  song_titles = [song['title'].lower() for song in data["songs"]]
  lowercased_song_name = song_name.lower()
  if lowercased_song_name in song_titles:
    song_index = song_titles.index(lowercased_song_name)
    lyrics = data['songs'][song_index]['lyrics']
    return find_sim(lyrics, data['songs'][song_index]['title'])

def _process_lyrics(lyrics: str):
        # Convert lyrics to lowercase and tokenize
        tokens = lyrics.lower().replace("(","").replace(")","").split()
        # Remove duplicate words
        unique_tokens = set(tokens)
        return unique_tokens


