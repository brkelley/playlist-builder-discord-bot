import os
import discord
from dotenv import load_dotenv
from config_handler import ConfigHandler
import os.path

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PORT = 4444
CHANNEL_ID = "992843220507697173"

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
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
    if str(reaction.emoji) == config.emoji:
        guild = client.get_guild(reaction.guild_id)
        channel = client.get_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)
        author = message.author
        actualAuthor = guild.get_member(author.id)
        # TODO handle this in the config
        role = guild.get_role(config.role)

        await actualAuthor.add_roles(role)

client.run(TOKEN)