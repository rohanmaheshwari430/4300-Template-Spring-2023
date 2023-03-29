import csv
from typing import List
import json


# Define a class to represent each song
class Song:
    def __init__(self, title: str, release_date: int, genre: List[str], lyrics: str):
        self.title = title.lower()
        self.release_date = release_date
        self.genre = genre
        self.lyrics = self._process_lyrics(lyrics)

    # Method to process lyrics
    def _process_lyrics(self, lyrics: str) -> List[str]:
        # Convert lyrics to lowercase and tokenize
        tokens = lyrics.lower().replace("(","").replace(")","").split()
        # Remove duplicate words
        unique_tokens = set(tokens)
        token_dict =  dict()
        for item in unique_tokens:
            token_dict[item]=1
        return token_dict

# Define the path to the CSV file
csv_file_path = 'data.csv'

# Open the CSV file
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(csv_file)
    data = {
        "songs":[]
    }
    songs=[]
    # Loop through each row in the CSV file
    for row in csv_reader:
        # Create a Song object for this row
        song = Song(title=row['Title'], release_date=(row['Date']), 
                    genre=row['Genres'].split(','), lyrics=row['Lyric'])
        person_json = {
            "title":song.title, 
            "release_date":song.release_date, 
            "genre":song.genre,
            "lyrics":song.lyrics
        }
        songs.append(person_json)
        print(person_json)
    data["songs"]=songs
    with open("data.json", "w") as f:
        json.dump(data, f)
