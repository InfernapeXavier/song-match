
# shows tracks for the given artist

# usage: python tracks.py [artist name]

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys

load_dotenv()


birdy_uri = 'spotify:artist:7vk5e3vY1uw9plTHJAMwjN'

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

results = sp.artist_albums(birdy_uri, album_type='single')
singles = results['items']
while results['next']:
    results = sp.next(results)
    singles.extend(results['items'])

albums.extend(singles)

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
