import os
import discord
from dotenv import load_dotenv
from threading import Thread
from flask import Flask
from functools import partial
from spotify_client import SpotifyClient
from discord_client import DiscordClient
from youtube import YoutubeClient
from urllib.parse import urlparse
from urllib.parse import parse_qs
import os.path

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PORT = 4444
CHANNEL_ID = "992843220507697173"
SPOTIFY_URL = "https://accounts.spotify.com/authorize?"

client = discord.Client()
spotifyClient = SpotifyClient()
youtubeClient = YoutubeClient()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if '!add' in message.content:
        # YouTube links
        if 'www.youtube.com' in message.content:
            youtube_url = message.content.split()[1]
            print('parsing YouTube link: ' + youtube_url)
            youtube_parsed_url = urlparse(youtube_url)
            youtube_id = parse_qs(youtube_parsed_url.query)['v'][0]
            video_title = youtubeClient.getVideoDetails(youtube_id)
            print('found song: ' + video_title)
            results = spotifyClient.searchSpotify(video_title)
            results_name = results['tracks']['items'][0]['name']
            results_artist = results['tracks']['items'][0]['artists'][0]['name']
            print('adding song: ', results_name)
            await message.channel.send('Adding ' + results_name + ' by ' + results_artist + ' to the playlist')
            spotifyClient.addToPlaylist(results['tracks']['items'][0]['id'])

        # Spotify links
        elif '!add' in message.content and 'spotify.com' in message.content:
            spotify_url = message.content.split()[1]
            print('parsing Spotify link: ' + spotify_url)
            spotify_parsed_path = urlparse(spotify_url).path
            track_id = os.path.split(spotify_parsed_path)[1]
            song = spotifyClient.getTrack(track_id)
            song_artist = song['artists'][0]['name']
            song_name = song['name']
            print('adding song to the playlist: ', song_name)
            await message.channel.send('Adding ' + song_name + ' by ' + song_artist + ' to the playlist')
            spotifyClient.addToPlaylist(track_id)

        # <song name> by <artist>
        else:
            if ' by ' not in message.content:
                await message.channel.send('No send it like this: "!add <song name> by <artist>"')

            results = spotifyClient.searchSpotify(message.content.replace(' by', ''))
            results_name = results['tracks']['items'][0]['name']
            results_artist = results['tracks']['items'][0]['artists'][0]['name']
            print('adding song: ', results_name)
            await message.channel.send('Adding ' + results_name + ' by ' + results_artist + ' to the playlist')
            spotifyClient.addToPlaylist(results['tracks']['items'][0]['id'])


# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return('', 204)

# partial_flask = partial(app.run, host="0.0.0.0", port=4444, debug=True, use_reloader=False)
# t = Thread(target=partial_flask)
# t.start()

client.run(TOKEN)