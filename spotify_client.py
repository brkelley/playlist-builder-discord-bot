import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os

FILE_NAME = 'spotify_info.json'

class SpotifyClient:
    def __init__(self) -> None:
        self.playlist_id = ''
        self.current_user_id = ''
        self.sp = None
        self.authorizeSpotify()
        self.loadSpotifyConfig()
        if (self.playlist_id == ''):
            self.createSpotifyRelics()

    def authorizeSpotify(self) -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="0d8a9dd56f844c988299f04101742d37",
                                               client_secret="",
                                               redirect_uri="http://localhost:8081/",
                                               scope="user-library-read playlist-modify-private"))

    def createSpotifyRelics(self) -> None:
        current_user = self.sp.me()
        self.current_user_id = current_user['id']
        print('Creating the playlist')
        playlist = self.sp.user_playlist_create(current_user['id'], 'build-a-vibe playlist', False, True, 'auto-generated playlist from the build-a-vibe bot')
        self.playlist_id = playlist['id']
        
        # Data to be written
        config = {
            "playlist_id": self.playlist_id
        }
        
        # Serializing json
        json_object = json.dumps(config, indent=4)
        
        # Writing to sample.json
        with open(FILE_NAME, "w") as outfile:
            outfile.write(json_object)

    def loadSpotifyConfig(self) -> None:
        # Opening JSON file
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                if 'playlist_id' in json_object:
                    self.playlist_id = json_object['playlist_id']
    
    def searchSpotify(self, searchString) -> None:
        return self.sp.search(searchString, 10, 0, 'track')
    
    def getTrack(self, track_id) -> None:
        return self.sp.track(track_id)

    def addToPlaylist(self, song_id) -> None:
        self.sp.playlist_add_items(self.playlist_id, [song_id])
