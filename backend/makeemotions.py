import text2emotion as te
import json
def store():
    f = open('data_cosine.json') # returns JSON object as a dictionary
    data = json.load(f)
    f.close()
    scores = {}
    b=0
    for song in data["songs"]:
      scores[song['title']]=list(te.get_emotion(song['lyrics']).values())
      b+=1
      print(b)
    with open('emotions.json', 'w') as f:
      json.dump(scores, f, ensure_ascii=False)
    
store() 