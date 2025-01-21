import discord
from discord.ext import commands
from discord import Embed
import lightbulb
import hikari

import os
import json
import asyncio
from youtube_dl import YoutubeDL
import youtube_dl
import requests

from dotenv import load_dotenv

TOKEN=os.getenv("TOKEN")

plugin = lightbulb.Plugin("Music", include_datastore = True)
bot = lightbulb.BotApp(
    TOKEN,
    intents=hikari.Intents.ALL,
    default_enabled_guilds=(988579939655778324, 890010030408093706,1009170512779431998, 686007857644175380, 1002009682338136076)
    )

# Function to search for YouTube videos using the YouTube Data API
def youtube_search(query):
    youtube_api_key = os.getenv("YTAPIKEY")
    url = f'https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&type=video&part=snippet&q={query}'
    response = requests.get(url)
    data = response.json()
    videos = []
    for item in data['items']:
        videos.append({
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId']
        })
    return videos

# Function to play the selected song in the voice channel
async def play_song(ctx, url):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.respond("You are not connected to a voice channel.")
        return
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        voice_client = await voice_channel.connect()
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
    voice_client.play(discord.FFmpegPCMAudio(url2))

# Command to play music
@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("song", "The name of the song (or url) that you want to play.", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("ytplay", "BINNY plays from yt.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ytplay(ctx: lightbulb.Context) -> None:
    query = ctx.options.song
    videos = youtube_search(query)
    embed = Embed(title="Search Results", description="Select a song to play:", color=0x00ff00)
    for i, video in enumerate(videos[:5], start=1):
        embed.add_field(name=f"**{i}.** {video['title']}", value=f"[Watch Video](https://www.youtube.com/watch?v={video['video_id']})", inline=False)
    message = await ctx.respond(embed=embed)
    for i in range(1, 6):
        await message.add_reaction(f"{i}\u20e3")
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [f"{i}\u20e3" for i in range(1, 6)]
    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=30, check=check)
        index = int(reaction.emoji[0]) - 1
        await play_song(ctx, f"https://www.youtube.com/watch?v={videos[index]['video_id']}")
    except asyncio.TimeoutError:
        await ctx.respond("You didn't select a song in time.")

# Command to skip the current song
@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("ytskip", "BINNY skips to the next song in queue.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ytskip(ctx: lightbulb.Context) -> None:
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None or not voice_client.is_playing():
        await ctx.respond("No song is currently playing.")
    else:
        voice_client.stop()
        await ctx.respond("Skipped the current song.")

# Command to display the queue
@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("ytqueue", "BINNY present the queue", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ytqueue(ctx: lightbulb.Context) -> None:
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None or not voice_client.is_playing():
        await ctx.respond("The queue is empty.")
    else:
        queue_info = "Current Queue:\n"
        for i, song in enumerate(ytqueue, start=1):
            queue_info += f"{i}. {song}\n"
        await ctx.respond(queue_info)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)