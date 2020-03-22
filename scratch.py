
# shows tracks for the given artist

# usage: python tracks.py [artist name]

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys

load_dotenv()


artistName = "Imagine Dragons"


client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Query to get artist URI
results = sp.search(q='artist:' + artistName, type='artist')
items = results['artists']['items']

if len(items) > 0:
    artist = items[0]
    urn = artist['uri']

birdy_uri = urn

results = sp.artist_albums(birdy_uri, album_type='album,single')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

li = list()


def show_album_tracks(album):
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for track in tracks:
        li.append(track['name'])


for album in albums:
    show_album_tracks(album)

li = set(li)
print(len(li))
# for x in li:
#     print(x)
