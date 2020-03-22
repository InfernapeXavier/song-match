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
db = client.song_match


def getArtistUri(artistName):
    # Query to get artist URI
    results = sp.search(q='artist:' + artistName, type='artist')
    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        uri = artist['uri']
    return uri


def topTenFetcher(artistName):
    # Fetches top 10 songs by artistName

    # Query to fetch top tracks
    uri = getArtistUri(artistName)
    response = sp.artist_top_tracks(uri)
    trackList = []
    for track in response['tracks']:
        trackList.append(track['name'])
    return trackList


def getTracksFromAlbum(album):
    tracks = []
    trackList = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for track in tracks:
        trackList.append(track['name'])
    return trackList


def allTracksFetcher(artistName):
    # Fetches all songs by artistName

    uri = getArtistUri(artistName)
    results = sp.artist_albums(uri, album_type='album,single')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    trackList = []
    for album in albums:
        trackList.extend(getTracksFromAlbum(album))
    print("here")
    return trackList


def countChecker(artistName):

    # creating/pointer new collection
    count = db.song_count

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


def getSongs(artistName):
    # gets the song name
    accessCount = countChecker(artistName)

    if accessCount < 10:
        tracks = topTenFetcher(artistName)
    else:
        tracks = allTracksFetcher(artistName)
    return tracks


def getUniqueSong(artistName):
    artist = db[artistName]
    exist = True
    songlist = db.songlist
    songData = songlist.find_one({"artist": artistName})

    trackslist = getSongs(artistName)

    if songData == None:
        newtracks = trackslist
    else:
        existingTracks = songData["tracks"]
        newtracks = set(trackslist).difference(set(existingTracks))
    newtracks = list(newtracks)
    track = secrets.choice(newtracks)
    insertSong(artistName, track)
    return track


def updateCount(artistName):
    count = db.song_count
    countData = count.update_one(
        {"artist": artistName}, {"$inc": {"count": 1}})


def getSongByAnswer(artistName, score):
    artist = db[artistName]
    song = artist.find_one({"answer": score})
    if song == None:
        track = getUniqueSong(artistName)
        songDocument = {
            "answer": score,
            "song": track
        }
        artist.insert_one(songDocument)
        updateCount(artistName)
        song = artist.find_one({"answer": score})
    return song["song"]


artist = "alan walker"
for score in range(0, 15):
    print(getSongByAnswer(artist, score))
