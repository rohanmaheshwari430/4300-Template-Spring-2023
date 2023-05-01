import json
import numpy as np
from typing import List
import os
import math 
import cosine_sim


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path_1 = os.path.join(script_dir, 'cossim_matrix_1.npy')
file_path_2 = os.path.join(script_dir, 'cossim_matrix_2.npy')
file_path_3 = os.path.join(script_dir, 'cossim_matrix_3.npy')

cossim_matrix_1 = np.load(file_path_1)
cossim_matrix_2 = np.load(file_path_2)
cossim_matrix_3 = np.load(file_path_3)

data_json_path = os.path.join(script_dir, 'data.json')
data_images_path = os.path.join(script_dir, 'data-images.json')

data_json = open(data_json_path) # if not use_images else open(data_images_path)
data_cosine_json = open(os.path.join(script_dir, 'data_cosine.json'))


data = json.load(data_json)
lyric_data = json.load(data_cosine_json)
data_json.close()
data_cosine_json.close()

emotionf = open(os.path.join(script_dir, 'emotions.json')) # returns JSON object as a dictionary
emotion_scores = json.load(emotionf)
emotionf.close()

def generalized_jaccard_similarity(s1, s2):
    s1_tokens = sum([s1[w] for w in s1.keys()])
    s2_tokens = sum([s2[w] for w in s2.keys()])
    good_types = set(s1.keys()).intersection(set(s2.keys()))
    if (len(good_types) == 0):
        return 0
    numerator = sum([min(s1[w] / s1_tokens, s2[w] / s2_tokens)
                    for w in good_types])
    denominator = sum([max(s1[w] / s1_tokens, s2[w] / s2_tokens)
                      for w in good_types])
    return numerator / denominator


def get_cossim(i, j):
    if i >= 0 and i < 1750:
        return cossim_matrix_1[i][j]
    if i >= 1750 and i < 3500:
        return cossim_matrix_2[i - 1750][j]
    if i >= 3500 and i <= 5250:
        return cossim_matrix_3[i - 3500][j]


def find_emotion_difference(arr1, arr2):
   difference = 0
   for i in range(0,5):
      difference = difference + ((arr1[i] - arr2[i]) * (arr1[i] - arr2[i]))
   return (1 - math.sqrt(difference / 5))
   
def find_similar_songs(query_song_lyrics, query_song_name, title_to_index, use_images):
    scores = []
    lyrics = {}
    for song in lyric_data["songs"]:
        lyrics[song['title']] = song['lyrics']

    for song in data["songs"]:
        if song["title"] != query_song_name:
            jaccard_score =  generalized_jaccard_similarity(query_song_lyrics, song['lyrics'])
            cossim_score = get_cossim(title_to_index[query_song_name], title_to_index[song['title']])
            score = 0
            if query_song_name in emotion_scores and song['title'] in emotion_scores:
                emotion_sim_score = find_emotion_difference(emotion_scores[query_song_name], emotion_scores[song['title']])
                popularity = song['popularity'] if song['popularity'] != None else 0
                score = (0.3 * jaccard_score) + (0.4 * cossim_score) + (0.2 * (popularity / 100)) + (0.1 * emotion_sim_score)
            else:
                popularity = song['popularity'] if song['popularity'] != None else 0
                score=(0.4 * jaccard_score) + (0.4 * cossim_score) + (0.2 * (popularity / 100))
            scores.append((song["title"], song['artist'], score, song['popularity']))

    scores.sort(key=lambda x: x[2], reverse=True)
    scores = scores[:10] 
    final_list = []
    i = 0
    if use_images:
        for (title, score, artist, genres, image) in scores:
            top_terms = cosine_sim.top_terms([query_song_name, title])
            final_list.append(({'title': title, 
                                'score': score,
                                'artist': artist, 
                                'genres': genres, 
                                'image': image, 
                              }))
            i += 1
    else:
        for (title, artist, score, popularity) in scores:
            score = round(score * 10, 1)
            top_terms = cosine_sim.top_terms([query_song_name, title])
            final_list.append(
                ({'title': title, 
                  'artist': artist, 
                  'score': str(score) + '/10', 
                  'lyrics': lyrics[title], 
                  'top_terms': top_terms, 
                  'popularity': popularity}))
            i += 1
    return final_list


def get_similar_songs(query_song_name, use_images):
    # returns JSON object as a dictionary
    f = open(
        data_json_path) if not use_images else open(data_images_path)
    data = json.load(f)
    title_to_index = {song['title']: i for i, song in enumerate(data['songs'])}

    # lowercase title matching
    song_titles = [song['title'].lower() for song in data["songs"]]
    lowercased_query_song_name = query_song_name.lower()
    if lowercased_query_song_name in song_titles:
        song_index = song_titles.index(lowercased_query_song_name)
        query_song_lyrics = data['songs'][song_index]['lyrics']
        # passing corrected title (case sensitive)
        return find_similar_songs(query_song_lyrics, data['songs'][song_index]['title'], title_to_index, use_images=None)


def autocorrect(query, use_images):
    # returns JSON object as a dictionary
    f = open(
        data_json_path) if not use_images else open(data_images_path)
    data = json.load(f)
    f.close()
    songs = [k['title'].lower() for k in data['songs']]
    r = edit_distance_search(query, songs)
    print("best results are ", r[:5])
    return r[0][1]


adj_chars = [('a', 'q'), ('a', 's'), ('a', 'z'), ('b', 'g'), ('b', 'm'), ('b', 'n'), ('b', 'v'), ('c', 'd'),
             ('c', 'v'), ('c', 'x'), ('d', 'c'), ('d', 'e'), ('d',
                                                              'f'), ('d', 's'), ('e', 'd'), ('e', 'r'),
             ('e', 'w'), ('f', 'd'), ('f', 'g'), ('f', 'r'), ('f',
                                                              'v'), ('g', 'b'), ('g', 'f'), ('g', 'h'),
             ('g', 't'), ('h', 'g'), ('h', 'j'), ('h', 'm'), ('h',
                                                              'n'), ('h', 'y'), ('i', 'k'), ('i', 'o'),
             ('i', 'u'), ('j', 'h'), ('j', 'k'), ('j', 'u'), ('k',
                                                              'i'), ('k', 'j'), ('k', 'l'), ('l', 'k'),
             ('l', 'o'), ('m', 'b'), ('m', 'h'), ('n', 'b'), ('n',
                                                              'h'), ('o', 'i'), ('o', 'l'), ('o', 'p'),
             ('p', 'o'), ('q', 'a'), ('q', 'w'), ('r', 'e'), ('r',
                                                              'f'), ('r', 't'), ('s', 'a'), ('s', 'd'),
             ('s', 'w'), ('s', 'x'), ('t', 'g'), ('t', 'r'), ('t',
                                                              'y'), ('u', 'i'), ('u', 'j'), ('u', 'y'),
             ('v', 'b'), ('v', 'c'), ('v', 'f'), ('w', 'e'), ('w',
                                                              'q'), ('w', 's'), ('x', 'c'), ('x', 's'),
             ('x', 'z'), ('y', 'h'), ('y', 't'), ('y', 'u'), ('z', 'a'), ('z', 'x')]


def substitution_cost(query, message, i, j):
    if query[i-1] == message[j-1]:
        return 0
    else:
        return 1.5 if (query[i - 1], message[j - 1]) in adj_chars else 2


def edit_matrix(query, message):

    m = len(query) + 1
    n = len(message) + 1

    chart = {(0, 0): 0}
    for i in range(1, m):
        chart[i, 0] = chart[i-1, 0] + 1
    for j in range(1, n):
        chart[0, j] = chart[0, j-1] + 1
    for i in range(1, m):
        for j in range(1, n):
            chart[i, j] = min(
                chart[i-1, j] + 1,
                chart[i, j-1] + 1,
                chart[i-1, j-1] + substitution_cost(query, message, i, j)
            )
    return chart


def edit_distance(query, message):
    return edit_matrix(query, message)[len(query), len(message)]


def edit_distance_search(query, msgs):
    return sorted([(edit_distance(query, msg), msg) for msg in msgs], key=lambda t: t[0])
