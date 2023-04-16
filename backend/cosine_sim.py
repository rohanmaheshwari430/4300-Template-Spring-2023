from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA
import json
import math

f = open('backend/data_cosine.json')
data = json.load(f) # returns JSON object as a dictionary

n_feats = 5000
doc_by_vocab = np.empty([len(data['songs']), n_feats])

title_to_index = {song['title']: i for i, song in enumerate(data['songs'])}

def build_vectorizer(max_features, stop_words, max_df=0.8, min_df=10, norm='l2'):
    return TfidfVectorizer(max_features=max_features,stop_words=stop_words, 
                           max_df=max_df, min_df=min_df, norm=norm)

def build_doc_by_vocab():
  tfidf_vec = build_vectorizer(n_feats, "english")
  doc_by_vocab = tfidf_vec.fit_transform([song['lyrics'] for song in data['songs']]).toarray()
  return doc_by_vocab

def build_index_to_vocab():
  tfidf_vec = build_vectorizer(n_feats, "english")
  index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}
  return index_to_vocab
   

def get_sim(song1, song2, input_doc_mat):
    s1_idx = title_to_index[song1]
    s2_idx = title_to_index[song2]
    
    s1_vector = input_doc_mat[s1_idx]
    s2_vector = input_doc_mat[s2_idx]
    
    numerator = np.dot(s1_vector, s2_vector)
    denominator = np.sqrt(np.dot(s1_vector, s1_vector)) * np.sqrt(np.dot(s2_vector, s2_vector))
    
    # Calculate the cosine similarity
    cossim = numerator / denominator
    print(song1, song2, cossim)
    return cossim

def top_terms(songs, input_doc_mat, index_to_vocab, title_to_index, top_k=10):
    song_indices = [title_to_index[song] for song in songs]
    prod_vec = np.prod(input_doc_mat[song_indices], axis=0)
    
    top_k_words_idx = prod_vec.argsort()[-top_k:][::-1]
    top_k_words = []
    for idx in top_k_words_idx:
        top_k_words.append(index_to_vocab[idx])
    
    return top_k_words
   

def build_song_sims_cos(title_to_index, input_get_sim_method):
  n_songs = len(data['songs'])
  song_sims = np.zeros((n_songs, n_songs))
  doc_mat = build_doc_by_vocab()

  for i in range(n_songs):
    for j in range(n_songs):
      song_sims[i][j] = input_get_sim_method(data['songs'][i]['title'], data['songs'][j]['title'], doc_mat)

  np.save('cossim_matrix.npy', song_sims)
  print('built and saved cossim matrix to file')
  return song_sims


song_sims_cos = build_song_sims_cos(title_to_index, get_sim)

