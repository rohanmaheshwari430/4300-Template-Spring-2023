import json
import azapi 
from typing import List


API = azapi.AZlyrics('google', accuracy=0.5)

def find_sim(lyrics:set,titleorig):
  f = open('data.json')
# returns JSON object as 
# a dictionary
  data = json.load(f)
  scores=[]
  for song in data["songs"]:
        if song["title"]!=titleorig:
          songlyrics = set(song["lyrics"].keys())
          intersection= songlyrics.intersection(lyrics)
          union=songlyrics.union(lyrics)
          if(len(union) == 0):
              scores.append((song["title"],0))
          else:
            score = len(intersection)/len(union)
            scores.append((song["title"],score))
  scores.sort(key = lambda x: x[1],reverse=True)
  scores=scores[:10]
  finallist=[]
  i =0
  for (title,scorey) in scores:
      finallist.append(({'title': title ,'score': scorey}))
      i+=1
  return finallist



def get_song_lyrics(song_name):
  API.title = song_name
  API.getLyrics(save=False)
  title=API.title
  return find_sim(_process_lyrics(API.lyrics),title)

def _process_lyrics( lyrics: str):
        # Convert lyrics to lowercase and tokenize
        tokens = lyrics.lower().replace("(","").replace(")","").split()
        # Remove duplicate words
        unique_tokens = set(tokens)
        return unique_tokens


get_song_lyrics('Bad Blod')

