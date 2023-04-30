import csv
from typing import List
import json


# Define a class to represent each song
class Song:
    def __init__(self, title: str, release_date: int, genre: List[str], lyrics: str, artist: str, album: str, year: int, length: float):
        self.title = title
        self.release_date = release_date
        self.genre = genre
        self.lyrics = lyrics
        self.artist = artist
        self.album = album
        self.year = year
        self.length = length

# Define the path to the CSV file
csv_file_path = 'exploration/data-combined.csv'

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
                    genre=row['Genres'].split(','), lyrics=row['Lyric'], 
                    artist=row['Artist'], year=row['Year'],
                    album=row['Album'], length=row['len']
                    )
        person_json = {
            "title": song.title, 
            "release_date": song.release_date, 
            "genre": song.genre,
            "lyrics": song.lyrics,
            "artist": song.artist,
            "year": song.year,
            "album": song.album,
            "length:": song.length
        }
        if ("remix" not in song.title.lower()) and ("dub" not in song.title.lower()):
          songs.append(person_json)
          print(person_json)
    data["songs"] = songs
    with open("backend/data_cosine.json", "w") as f:
        json.dump(data, f)