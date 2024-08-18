# This example requires the 'message_content' privileged intent to function.

import asyncio

import discord
import youtube_dl

from discord.ext import commands
import mutagen
import ffmpeg
import ffprobe
import math
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

prev_channel = '0'
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        global prev_channel
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        elif ctx.message.author.voice.channel.id == prev_channel:
            pass
        else:
            channel = ctx.message.author.voice.channel
            prev_channel = ctx.message.author.voice.channel.id
            await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        await self.join(ctx)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.reply(f'Now playing: {query}')

    @commands.command()
    async def sound(self, ctx, *, query):
        query = f'data/sounds/{query}'
        await self.join(ctx)
        print(f'Playing {query}')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else self.bot.loop.create_task(ctx.voice_client.disconnect()))
        await ctx.reply(f'Now playing: {query}')

    @commands.command()
    async def length(self, ctx, query):
        """get length"""
        probe = ffmpeg.probe(query, cmd='ffprobe')
        stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        duration = float(stream['duration'])
        print(f'This song is {duration}s long.')
        ctx.reply(f'This song is {duration}s long.')
        duration = math.ceil(duration)
        return duration

    @commands.command()
    async def playloop(self, ctx, query):
        """Plays a file from the local filesystem in loop"""
        query = f'data/sounds/Music/{query}'
        await ctx.send(f'Now playing: {query}')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else self.bot.loop.create_task(self.playloop(ctx, query)))
            

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.reply('cya mate')
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))