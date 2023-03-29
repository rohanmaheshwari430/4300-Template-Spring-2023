import json
from typing import List



def find_sim(query_song_lyrics, query_song_name, use_images):
  f = open('data.json') if not use_images else open('data-images.json')# returns JSON object as a dictionary
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
            if not use_images:
              scores.append((song["title"], score))
            else:
              scores.append((song["title"], score, song["artist"], song["genres"], song["image"]))
  scores.sort(key = lambda x: x[1],reverse=True)
  scores = scores[:10]
  final_list = []
  i = 0
  if use_images:
      for (title,score, artist, genres, image) in scores:
        final_list.append(({'title': title ,'score': score, 'artist': artist, 'genres': genres, 'image': image}))
        i += 1
  else:
    for (title,score) in scores:
        final_list.append(({'title': title ,'score': score}))
        i += 1
  return final_list



def get_song_lyrics(query_song_name, use_images):
  f = open('data.json') if not use_images else open('data-images.json')# returns JSON object as a dictionary
  data = json.load(f)
  # lowercase title matching 
  song_titles = [song['title'].lower() for song in data["songs"]]
  lowercased_query_song_name = query_song_name.lower()
  if lowercased_query_song_name in song_titles:
    song_index = song_titles.index(lowercased_query_song_name)
    query_song_lyrics = data['songs'][song_index]['lyrics']
    return find_sim(query_song_lyrics, data['songs'][song_index]['title'], use_images) # passing corrected title (case sensitive) 

def _process_lyrics(lyrics: str):
        # Convert lyrics to lowercase and tokenize
        tokens = lyrics.lower().replace("(","").replace(")","").split()
        # Remove duplicate words
        unique_tokens = set(tokens)
        return unique_tokens


