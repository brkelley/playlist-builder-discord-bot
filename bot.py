import os
import discord
from dotenv import load_dotenv
from threading import Thread
from flask import Flask
from functools import partial
from spotify_client import SpotifyClient
from config_handler import ConfigHandler
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
config = ConfigHandler()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if '!configure' in message.content:
        if 'setemoji' in message.content:
            chosen_emoji = message.content.split(' ')[2]
            config.setEmoji(chosen_emoji)
            await message.add_reaction('✅')
        elif 'setrole' in message.content:
            chosen_role = message.content.split(' ')[2]
            config.setRole(chosen_role)
            await message.add_reaction('✅')
    
@client.event
async def on_raw_reaction_add(reaction):
    print(str(reaction.emoji))
    if str(reaction.emoji) == config.emoji:
        guild = client.get_guild(reaction.guild_id)
        print(guild)
        channel = client.get_channel(reaction.channel_id)
        print(channel)
        message = await channel.fetch_message(reaction.message_id)
        print(message)
        author = message.author
        author.add_roles(client.role)
    
    # if '!add' in message.content:
    #     # YouTube links
    #     if 'www.youtube.com' in message.content:
    #         youtube_url = message.content.split()[1]
    #         print('parsing YouTube link: ' + youtube_url)
    #         youtube_parsed_url = urlparse(youtube_url)
    #         youtube_id = parse_qs(youtube_parsed_url.query)['v'][0]
    #         video_title = youtubeClient.getVideoDetails(youtube_id)
    #         print('found song: ' + video_title)
    #         results = spotifyClient.searchSpotify(video_title)
    #         results_name = results['tracks']['items'][0]['name']
    #         results_artist = results['tracks']['items'][0]['artists'][0]['name']
    #         print('adding song: ', results_name)
    #         await message.channel.send('Adding ' + results_name + ' by ' + results_artist + ' to the playlist')
    #         spotifyClient.addToPlaylist(results['tracks']['items'][0]['id'])

    #     # Spotify links
    #     elif '!add' in message.content and 'spotify.com' in message.content:
    #         spotify_url = message.content.split()[1]
    #         print('parsing Spotify link: ' + spotify_url)
    #         spotify_parsed_path = urlparse(spotify_url).path
    #         track_id = os.path.split(spotify_parsed_path)[1]
    #         song = spotifyClient.getTrack(track_id)
    #         song_artist = song['artists'][0]['name']
    #         song_name = song['name']
    #         print('adding song to the playlist: ', song_name)
    #         await message.channel.send('Adding ' + song_name + ' by ' + song_artist + ' to the playlist')
    #         spotifyClient.addToPlaylist(track_id)

    #     # <song name> by <artist>
    #     else:
    #         if ' by ' not in message.content:
    #             await message.channel.send('No send it like this: "!add <song name> by <artist>"')

    #         results = spotifyClient.searchSpotify(message.content.replace(' by', ''))
    #         results_name = results['tracks']['items'][0]['name']
    #         results_artist = results['tracks']['items'][0]['artists'][0]['name']
    #         print('adding song: ', results_name)
    #         await message.channel.send('Adding ' + results_name + ' by ' + results_artist + ' to the playlist')
    #         spotifyClient.addToPlaylist(results['tracks']['items'][0]['id'])


# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return('', 204)

# partial_flask = partial(app.run, host="0.0.0.0", port=4444, debug=True, use_reloader=False)
# t = Thread(target=partial_flask)
# t.start()

client.run(TOKEN)