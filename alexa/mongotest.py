from pymongo import MongoClient
import pymongo
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from dotenv import load_dotenv
from pprint import pprint
import secrets

# Loading Spotify API Data from Env
load_dotenv()

# spotipy credentials manager
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# creating mongo client
client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0-jgksl.mongodb.net/test?retryWrites=true&w=majority")

# Creating/Pointer new db
db = client.song_match
