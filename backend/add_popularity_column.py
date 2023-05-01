import json
import os
import requests
import time

CLIENT_ID = 'f3daab45338c4952b3dcb553b42f77ab'
CLIENT_SECRET = '4a5c428ccb444ec088f0e90bc798f683'

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/search'

def get_headers():
  auth_response = requests.post(AUTH_URL, {'grant_type': 'client_credentials', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,})
  auth_response_data = auth_response.json()
  access_token = auth_response_data['access_token']
  headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
  return headers

def get_song_popularity(query_song_name, headers):
    r = requests.get(BASE_URL, params={'q': query_song_name, 'type': 'track', 'limit': 1}, headers=headers)
    r = r.json()
    try:
        return r['tracks']['items'][0]['popularity']
    except:
        print("Error: ", r)
        if(len(r['tracks']['items']) == 0):
            return None
        else:
          print(" ")
          print("---------- refreshing access token and creating new headers ----------")
          print(" ")
          new_headers = get_headers()
          get_song_popularity(query_song_name, new_headers)

    
def add_popularity_column(headers):
    data_json = open(os.path.join(os.path.dirname(__file__), 'data.json'))
    data = json.load(data_json)
    data_json.close()
    for song in data['songs']:
        song['popularity'] = get_song_popularity(song['title'], headers)
        print(song['title'], song['popularity'])
        time.sleep(0.3)
    data_json = open('backend/data.json', 'w')
    json.dump(data, data_json)
    data_json.close()
    
def main():
    headers = get_headers()
    add_popularity_column(headers)

main()

