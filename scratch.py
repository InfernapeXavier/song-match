#  Scratch File to test logic

from pathlib import Path  # python3 only
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from dotenv import load_dotenv

# Loading Spotify API Data from Env
load_dotenv()

if len(sys.argv) > 1:
    urn = sys.argv[1]
else:
    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
response = sp.artist_top_tracks(urn)

for track in response['tracks']:
    print(track['name'])
