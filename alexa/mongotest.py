from pymongo import MongoClient
import pymongo
import datetime
from pathlib import Path  # python3 only
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from dotenv import load_dotenv
from pprint import pprint

# Loading Spotify API Data from Env
load_dotenv()

# spotipy credentials manager
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# creating mongo client
client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0-jgksl.mongodb.net/test?retryWrites=true&w=majority")


def songFetcher(artistName):
    # Fetches top 10 songs by artistName

    # Query to getartist URI
    results = sp.search(q='artist:' + artistName, type='artist')
    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        urn = artist['uri']

    # Query to fetch top tracks
    response = sp.artist_top_tracks(urn)
    trackList = []
    for track in response['tracks']:
        trackList.append(track['name'])
    return trackList


def countChecker(artistName):

    # Creating/Pointer new db
    db = client.songMatch

    # creating/pointer new collection
    count = db.count

    # fetch artist counter
    countData = count.find_one({"artist": artistName})
    if countData == None:

        # create count data for artist

        # defining document
        countDocument = {
            "artist": artistName,
            "count": 0
        }

        # inserting document
        count.insert_one(countDocument)
        countData = count.find_one({"artist": artistName})
    accessCount = countData["count"]
    return accessCount


def getSong(artistName):
    # gets the song name
    accessCount = countChecker(artistName)
