import json
from typing import List

def generalized_jaccard_similarity(s1, s2):
    s1_tokens = sum([s1[w] for w in s1.keys()])
    s2_tokens = sum([s2[w] for w in s2.keys()])
    good_types = set(s1.keys()).intersection(set(s2.keys()))
    if(len(good_types) == 0):
       return 0
    numerator = sum([min(s1[w] / s1_tokens, s2[w] / s2_tokens) for w in good_types])
    denominator = sum([max(s1[w] / s1_tokens, s2[w] / s2_tokens) for w in good_types])
    if(numerator / denominator == 1):
       print("num dem: ", numerator, denominator)
    return numerator / denominator

def find_sim(query_song_lyrics, query_song_name, use_images):
  f = open('backend/data.json') if not use_images else open('backend/data-images.json')# returns JSON object as a dictionary
  data = json.load(f)
  scores = []
  for song in data["songs"]:
        if song["title"] != query_song_name:
          score =  generalized_jaccard_similarity(query_song_lyrics, song['lyrics'])
          scores.append((song["title"], score))
          #   if not use_images:
          #     scores.append((song["title"], score))
          #   else:
          #     scores.append((song["title"], score, song["artist"], song["genres"], song["image"]))
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
        score = round(score * 10, 1)
        final_list.append(({'title': title ,'score': str(score) + '/10'}))
        i += 1
  return final_list



def get_song_lyrics(query_song_name, use_images):
  f = open('backend/data.json') if not use_images else open('backend/data-images.json')# returns JSON object as a dictionary
  data = json.load(f)
  # lowercase title matching 
  song_titles = [song['title'].lower() for song in data["songs"]]
  lowercased_query_song_name = query_song_name.lower()
  if lowercased_query_song_name in song_titles:
    song_index = song_titles.index(lowercased_query_song_name)
    query_song_lyrics = data['songs'][song_index]['lyrics']
    return find_sim(query_song_lyrics, data['songs'][song_index]['title'], use_images=None) # passing corrected title (case sensitive) 


