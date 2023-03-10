import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import os
import time

from dotenv import load_dotenv

load_dotenv()

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

intents = discord.Intents().all()
client = commands.Bot(command_prefix='-', intents=intents)


@client.command()
async def play(ctx, *, arg):
    vc = await ctx.message.author.voice.channel.connect()

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in arg:
            info = ydl.extract_info(arg, download=False)
        else:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

    url = info['formats'][0]['url']

    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@client.command(name='test')
async def test(ctx):
    pass

@client.command()
async def send(ctx, member:discord.Member, n:int, text:str = None):
    if text is None:
        channel_id = ctx.channel.id
        channel = client.get_channel(channel_id)
        for i in range(n, 0, -1):
            await channel.send(f'<@{member.id}>')
            time.sleep(1)
    else:
        channel_id = ctx.channel.id
        channel = client.get_channel(channel_id)
        for i in range(n, 0, -1):
            await channel.send(f'<@{member.id}> {text}')
            time.sleep(1)

client.run(os.getenv('TOKEN'))