#  Scratch File to test logic

from pathlib import Path  # python3 only
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from dotenv import load_dotenv

# Loading Spotify API Data from Env
load_dotenv()

name = 'Bastille'


sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = sp.search(q='artist:' + name, type='artist')
items = results['artists']['items']

if len(items) > 0:
    artist = items[0]
    urn = artist['uri']

response = sp.artist_top_tracks(urn)

for track in response['tracks']:
    print(track['name'])
