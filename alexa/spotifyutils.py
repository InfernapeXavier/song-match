from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv
import sys

# Loading Spotify API Data from Env
load_dotenv()

# spotipy credentials manager
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def getArtistUri(artistName):
    # Query to get artist URI
    results = sp.search(q='artist:' + artistName, type='artist')
    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        uri = artist['uri']
    return uri


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


def topTenFetcher(artistName):
    # Fetches top 10 songs by artistName

    # Query to fetch top tracks
    uri = getArtistUri(artistName)
    response = sp.artist_top_tracks(uri)
    trackList = []
    for track in response['tracks']:
        trackList.append(track['name'])
    return trackList
