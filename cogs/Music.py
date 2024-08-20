# This example requires the 'message_content' privileged intent to function.

import asyncio

import discord
import youtube_dl

from discord.ext import tasks, commands
import ffmpeg
import ffprobe
import math
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

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

# 指定しておかないとなんか動かない者たち

duration = float(0)

zunda = 'https://i.imgur.com/6bgRNLR.png'

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

    async def join(self, ctx):
        """Joins a voice channel"""
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
            return
        else:
            channel = ctx.message.author.voice.channel
            try:
                await channel.connect()
            except:
                pass

    def get_mp3_thumbnail(self, file_path):
        audio = MP3(file_path, ID3=ID3)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                with open("data/thumbnail.jpg", "wb") as img:
                    img.write(tag.data)
                return "data/thumbnail.jpg"
        return None

    async def embed(self, ctx, query, player_loop=False):
        """Makes embed for reply"""
        # emojify T/F
        if player_loop == True:
            player_loop = str('✅')
        else:
            player_loop = str('❌')

        # カバーアート情報取得
        thumbnail_path = self.get_mp3_thumbnail(file_path=query)
        if thumbnail_path:
            print(f"サムネイルを保存しました: {thumbnail_path}")
        else:
            print("サムネイルが見つかりませんでした。")
        global music_embed
        self.music_embed = discord.Embed( # Embedを定義する
                              title = "Now Playing...",# タイトル
                              color = 0x191919, # フレーム色指定
                              description = f'{query}\nLooping: {player_loop}', # Embedの説明文
                              )
        self.music_embed.set_author(name = 'ローカルファイル再生Bot', # Botのユーザー名
                         url = "https://satt.carrd.co/", # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
                         icon_url = zunda # Botのアイコンを設定してみる
                         )
        self.music_embed.set_thumbnail(url = "attachment://image.jpg") # サムネイルとして小さい画像を設定できる
        self.music_embed.set_footer(text = "Pasted by Satt", # フッターには開発者の情報でも入れてみる
                                icon_url = zunda)
        file = discord.File(thumbnail_path, filename="temp.jpg")
        self.music_embed.set_image(url="attachment://image.jpg")
        await ctx.reply(embed=self.music_embed, file=file)

    @commands.command()
    async def call(self,ctx):
        await self.join(ctx)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("Data/sounds/カードが必要なら.wav"))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

    @commands.command()
    async def play(self, ctx, query, player_loop=False):
        """Plays a file from the local filesystem"""
        await self.embed(ctx, query=query, player_loop=player_loop)
        if player_loop == True:
            global loop
            loop = True
            await self.join(ctx)
            while True:
                if ctx.voice_client.is_playing():
                    await asyncio.sleep(0.01)
                else:
                    if loop == True:
                        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
                        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
                    else:
                        break
            await self.stop(ctx)
        else:
            await self.join(ctx)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
            ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

    @commands.command()
    async def sound(self, ctx, *, query):
        query = f'data/sounds/{query}'
        await self.join(ctx)
        print(f'Playing {query}')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else self.bot.loop.create_task(self.stop(ctx)))
        await ctx.reply(embed=await self.embed(ctx, query=query))
        global prev_channel

    @commands.command()
    async def length(self, ctx, query):
        """get length"""
        probe = ffmpeg.probe(query, cmd='ffprobe')
        stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        global duration
        duration = float(stream['duration'])
        print(f'This song is {duration}s long.')
        await ctx.reply(f'This song is {duration}s long.')
        return duration
        
    @commands.command()
    async def loop(self, ctx):
        """omg! loop feature"""
        global loop
        loop = False
        await ctx.reply('aight bro its gonna stop as soon as this track ends')

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
        await ctx.reply('Player done!')
        await ctx.voice_client.disconnect()
        global prev_channel
        prev_channel = '0'

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