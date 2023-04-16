import json
import numpy as np
from typing import List

cossim_matrix_1 = np.load('backend/cossim_matrix_1.npy')
cossim_matrix_2 = np.load('backend/cossim_matrix_2.npy')
cossim_matrix_3 = np.load('backend/cossim_matrix_3.npy')

def generalized_jaccard_similarity(s1, s2):
    s1_tokens = sum([s1[w] for w in s1.keys()])
    s2_tokens = sum([s2[w] for w in s2.keys()])
    good_types = set(s1.keys()).intersection(set(s2.keys()))
    if(len(good_types) == 0):
       return 0
    numerator = sum([min(s1[w] / s1_tokens, s2[w] / s2_tokens) for w in good_types])
    denominator = sum([max(s1[w] / s1_tokens, s2[w] / s2_tokens) for w in good_types])
    print(numerator / denominator)
    return numerator / denominator

def get_cossim(i,j):
  if i >= 0 and i < 1750:
     return cossim_matrix_1[i][j]
  if i >= 1750 and i < 3500:
     return cossim_matrix_2[i - 1750][j]
  if i >= 3500 and i <= 5250:
     return cossim_matrix_3[i - 3500][j]

def find_sim(query_song_lyrics, query_song_name, title_to_index, use_images):
  f = open('backend/data.json') if not use_images else open('backend/data-images.json')# returns JSON object as a dictionary
  data = json.load(f)
  scores = []
  for song in data["songs"]:
        if song["title"] != query_song_name:
          jaccard_score =  generalized_jaccard_similarity(query_song_lyrics, song['lyrics'])
          cossim_score = get_cossim(title_to_index[query_song_name], title_to_index[song['title']])
          score = (0.6 * jaccard_score) + (0.4 * cossim_score)
          scores.append((song["title"], song['artist'], score))
          #   if not use_images:
          #     scores.append((song["title"], score))
          #   else:
          #     scores.append((song["title"], score, song["artist"], song["genres"], song["image"]))
  scores.sort(key = lambda x: x[2],reverse=True)
  scores = scores[:10]
  final_list = []
  i = 0
  if use_images:
      for (title,score, artist, genres, image) in scores:
        final_list.append(({'title': title ,'score': score, 'artist': artist, 'genres': genres, 'image': image}))
        i += 1
  else:
    for (title, artist, score) in scores:
        score = round(score * 10, 1)
        final_list.append(({'title': title , 'artist': artist, 'score': str(score) + '/10'}))
        i += 1
  print(final_list)
  return final_list

def get_song_lyrics(query_song_name, use_images):
  f = open('backend/data.json') if not use_images else open('backend/data-images.json')# returns JSON object as a dictionary
  data = json.load(f)
  title_to_index = {song['title']: i for i, song in enumerate(data['songs'])}
  # lowercase title matching 
  song_titles = [song['title'].lower() for song in data["songs"]]
  lowercased_query_song_name = query_song_name.lower()
  if lowercased_query_song_name in song_titles:
    song_index = song_titles.index(lowercased_query_song_name)
    query_song_lyrics = data['songs'][song_index]['lyrics']
    return find_sim(query_song_lyrics, data['songs'][song_index]['title'], title_to_index, use_images=None) # passing corrected title (case sensitive) 