from pathlib import Path  # python3 only
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from dotenv import load_dotenv

# Loading Spotify API Data from Env
load_dotenv()

# spotipy credentials manager
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


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


def getIndex(score):
    if score == '111':
        return 0
    if score == '112':
        return 1
    if score == '121':
        return 2
    if score == '122':
        return 3
    if score == '211':
        return 4
    if score == '212':
        return 5
    if score == '221':
        return 6
    if score == '222':
        return 7
