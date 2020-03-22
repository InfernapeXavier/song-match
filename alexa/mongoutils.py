from pymongo import MongoClient
import pymongo
from pprint import pprint
import secrets
from alexa import spotifyutils

# connecting mongo client
client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0-jgksl.mongodb.net/test?retryWrites=true&w=majority")

# Creating/Pointer new db
db = client.song_match


def countChecker(artistName):
    # creating/pointer new collection
    count = db.song_count

    # fetch artist counter
    countData = count.find_one({"artist": artistName})
    if countData == None:

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


def updateCount(artistName):
    count = db.song_count
    countData = count.update_one(
        {"artist": artistName}, {"$inc": {"count": 1}})


def getSongs(artistName):
    # gets the song name
    accessCount = countChecker(artistName)

    if accessCount < 10:
        tracks = spotifyutils.topTenFetcher(artistName)
    else:
        tracks = spotifyutils.allTracksFetcher(artistName)
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
