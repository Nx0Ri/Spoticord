import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = 'client_id'
SPOTIPY_CLIENT_SECRET = 'client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

scope = "user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def get_current_track():
    current_track = sp.current_playback()
    if current_track is not None and current_track['is_playing']:
        track = current_track['item']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        return track_name, artist_name, True
    return None, None, False

if __name__ == "__main__":
    track, artist, is_playing = get_current_track()