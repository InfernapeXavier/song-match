from pymongo import MongoClient
import pymongo
import datetime
from pathlib import Path  # python3 only
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
db = client.songMatch


def topTenFetcher(artistName):
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


def insertSong(artistName, song):
    songlist = db.songlist
    listData = songlist.find_one({"artist": artistName})
    li = []
    li.append(song)
    if listData == None:
        listDocument = {
            "artist": artistName,
            "tracks": li
        }
        songlist.insert_one(listDocument)
    else:
        listData = songlist.update_one(
            {"artist": artistName},
            {"$addToSet": {"tracks": song}}
        )


def getSong(artistName):
    # gets the song name
    accessCount = countChecker(artistName)

    if accessCount < 10:
        tracks = topTenFetcher(artistName)
        song = secrets.choice(tracks)
        insertSong(artistName, song)
        return song
    else:
        return ("More than 10")


def getUniqueSong(artistName):
    artist = db[artistName]
    exist = True
    while exist:
        track = getSong(artistName)
        count = artist.count_documents({"song": track})
        if count == 0:
            exist = False
    return track


def updateCount(artistName):
    count = db.count
    countData = count.update_one(
        {"artist": artistName}, {"$inc": {"count": 1}})


def getSongByAnswer(artistName, score):
    artist = db[artistName]
    updateCount(artistName)
    song = artist.find_one({"answer": score})
    if song == None:
        track = getUniqueSong(artistName)
        songDocument = {
            "answer": score,
            "song": track
        }
        artist.insert_one(songDocument)
        song = artist.find_one({"answer": score})
    return song["song"]


artist = "alan walker"
for score in range(0, 11):
    print(getSongByAnswer(artist, score))
