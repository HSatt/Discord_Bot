import asyncio

import discord
import youtube_dl
import random
from discord.ext import tasks, commands
import ffmpeg
import ffprobe
import math
from mutagen.flac import FLAC, Picture
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen import MutagenError
import os
from cogs.diyembed import diyembed
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

waste = 1275277189230628914 # ゴミ捨て場

music_queue = []

path = "data/sounds"
dirs = [f for f in os.listdir(path) if os.path.isdir(path + "/" + f)]
voices = []

def getmefiles(file):
    while True:
        sub_files = os.listdir(path + "/" + dir + "/" + file)
        print(sub_files)
        for sub_file in sub_files:
            if not "." in sub_file:
                print(f"File detected! {sub_file}")
                getmefiles(file=(file + "/" + sub_file))
            else:
                file_path = str(dir + "/" + file + "/" + sub_file).lower()
                voices.append(file_path)
        break

for dir in dirs:
    if dir == "venv":
        continue
    files = os.listdir(path + "/" + dir)
    for file in files:
        if not "." in file:
            print(f"File detected! {file}")
            getmefiles(file)
        else:
            file_path = str(dir + "/" + file).lower()
            voices.append(file_path)

cpath = "C://Users/hatos/Music"
cdirs = [f for f in os.listdir(cpath) if os.path.isdir(cpath + "/" + f)]
cvoices = []

def cgetmefiles(file):
    while True:
        sub_files = os.listdir(cpath + "/" + cdir + "/" + file)
        for sub_file in sub_files:
            if not "." in sub_file:
                cgetmefiles(file=(file + "/" + sub_file))
            else:
                file_path = str(cdir + "/" + file + "/" + sub_file).lower()
                cvoices.append(file_path)
        break

for cdir in cdirs:
    if cdir == "Music":
        continue
    files = os.listdir(cpath + "/" + cdir)
    for file in files:
        if not "." in file:
            print(f"File detected! {file}")
            cgetmefiles(file)
        else:
            file_path = str(cdir + "/" + file).lower()
            cvoices.append(file_path)

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
            await ctx.send(f" You are not connected to a voice channel")
            return
        else:
            channel = ctx.message.author.voice.channel
            try:
                await channel.connect()
            except Exception as e:
                print(e)
                pass

    def get_mp3_thumbnail(self, file_path):
        audio = MP3(file_path, ID3=ID3)
        try:
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    with open("data/thumbnail.jpg", "wb") as img:
                        img.write(tag.data)
                    return "data/thumbnail.jpg"
        except AttributeError:
            return None
        
    def get_flac_thumbnail(self, file_path):
        audio = FLAC(file_path)
        try:
            for picture in audio.pictures:
                with open("data/thumbnail.jpg", "wb") as img:
                    img.write(picture.data)
                return "data/thumbnail.jpg"
        except AttributeError:
            return None

    async def prep_embed(self, ctx, query, player_loop=False):
        """Makes embed for reply"""
        # emojify T/F
        if player_loop == True:
            player_loop = str('✅')
        else:
            player_loop = str('❌')

        # カバーアート情報取得
        if query.endswith(".flac") == True:
            thumbnail_path = self.get_flac_thumbnail(file_path=query)
        elif query.endswith(".mp3") == True:
            thumbnail_path = self.get_mp3_thumbnail(file_path=query)
        else:
            thumbnail_path = None
        if thumbnail_path:
            print(f"サムネイルを保存しました: {thumbnail_path}")
        else:
            print("サムネイルが見つかりませんでした。")
        
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
        if thumbnail_path:
            file = discord.File(thumbnail_path, filename="temp.jpg")
            self.music_embed.set_image(url='attachment://temp.jpg')
            await ctx.reply(file=file, embed=self.music_embed)
        else:
            await ctx.reply(embed=self.music_embed)

    @commands.command()
    async def call(self, ctx):
        await self.join(ctx)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("Data/sounds/soundboard/カードが必要なら.wav"))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

    @commands.command()
    async def play(self, ctx, query="", player_loop=False):
        """Plays a file from the local filesystem"""
        query = await self.search(ctx, query)
        await self.join(ctx)
        for content in query:
            content = path + "/" + content
            await self.prep_embed(ctx, query=content, player_loop=player_loop)
            music_queue.append(content)
            print(music_queue)
            if not ctx.voice_client.is_playing():
                await self.player(ctx, current=0, loop=player_loop)

    @commands.command()
    async def cplay(self, ctx, query="", player_loop=False):
        query = await self.csearch(ctx, query)
        print(query)
        await self.join(ctx)
        for content in query:
            content = cpath + "/" + content
            await self.prep_embed(ctx, query=content, player_loop=player_loop)
            music_queue.append(content)
            print(music_queue)
            if not ctx.voice_client.is_playing():
                await self.player(ctx, current=0, loop=player_loop)

    @commands.command()
    async def shuffle(self, ctx):
        random.shuffle(music_queue)
        await ctx.reply('Queue shuffled!')
        await self.getq(ctx)

    async def player(self, ctx, current, loop=False):
        if loop == True:
            try:
                print(music_queue[current])
            except IndexError:
                current = 0
                print(music_queue[current])
            source = music_queue[current]
            current += 1
        else:
            try:
                print(music_queue[0])
            except IndexError:
                await ctx.reply('No more songs in queue!')
                await self.stop(ctx)
                return
            source = music_queue.pop(0)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source))
        ctx.voice_client.play(source, 
                              after=lambda e: print(f'Player error: {e}') if e else self.bot.loop.create_task(self.player(ctx, current=current, loop=loop)))

    @commands.command()
    async def getq(self, ctx):
        reciept = ''
        for raw_item in music_queue:
            getq_response = ''
            for thing in raw_item.split('/'):
                if not thing in cpath:
                    getq_response += thing + '/'
            reciept += f'- {getq_response}\n'
        try:
            await ctx.reply(embed=await diyembed.getembed(self, title="Queue", color=0x1084fd, description=f"{reciept}",))
        except discord.HTTPException:
            await ctx.reply(f"うわーん！リストが長すぎます！ このレシートは{len(reciept)}mです！")
            print(f"this result contains: {len(reciept)} characters")
            first = False
            for i in range(math.floor(len(reciept) / 3500)):
                for check in range(500):
                    if str(reciept[3500 * (i + 1) + check]) == str("-"):
                        check -= 1
                        if first == True:
                            await ctx.send(embed=await diyembed.getembed(self, color=0x1084fd,
                                                                         description=reciept[3500 * (i) + prev_check:3500 * (i + 1) + check],  
                                                                            ))
                        if first == False:
                            await ctx.send(embed=await diyembed.getembed(self, title=f"Queue", color=0x1084fd, 
                                                                            description=reciept[:3500 + check], 
                                                                            author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                                            author_icon=zunda, thumbnail=zunda,
                                                                            ))
                            first = True
                        prev_check = check
                        break
            await ctx.send(embed=await diyembed.getembed(self, color=0x1084fd, 
                                                                      description=reciept[3500 * (i + 1) + check:],
                                                                      footer_text="Pasted by Satt", footer_icon=zunda))

    @commands.command()
    async def sound(self, ctx, query):
        query = f'soundboard/{query}'
        await self.play(ctx, query=query)

    async def fetch(self, ctx, query, raw_result):
        removed = []
        for item in raw_result:
            if item.endswith(".jpg") or item.endswith(".png") or item.endswith(".jpeg"):
                removed.append(item)
        for removeitem in removed:
            raw_result.remove(removeitem)
        result = ''
        if raw_result == []:
            await ctx.reply('No results found!')
            return raw_result
        result += f'{raw_result[0].split('/')[0]}\n'
        for directory in raw_result:
            if not "." in directory.split('/')[1]:
                count = 1
                while True:
                    for test in directory.split('/'):
                        if not test in result:
                            result += f'ᅠ' * (count) + f'┗{test}\n'
                            if "." in test:
                                break
                        count += 1
                    break
            else:
                result += f'┗{directory.split('/')[1]}\n'
        try:
            await ctx.reply(embed=await diyembed.getembed(self, title=f"""You searched for "{query}"...""", color=0x1084fd, description=result, 
                        author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', author_icon=zunda, thumbnail=zunda,
                        footer_text="Pasted by Satt", footer_icon=zunda))
        except discord.HTTPException:
            await ctx.reply(f"うわーん！リストが長すぎます！ このレシートは{len(result)}mです！")
            print(f"this result contains: {len(result)} characters")
            first = False
            for i in range(math.floor(len(result) / 3500)):
                for check in range(500):
                    if str(result[3500 * (i + 1) + check:3500 * (i + 1) + check + 1]) == str("\n"):
                        if first == True:
                            await ctx.send(embed=await diyembed.getembed(self, color=0x1084fd,
                                                                         description=result[3500 * (i) + prev_check:3500 * (i + 1) + check],  
                                                                            ))
                        if first == False:
                            await ctx.send(embed=await diyembed.getembed(self, title=f"""You searched for "{query}"...""", color=0x1084fd, 
                                                                            description=result[:3500 + check], 
                                                                            author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                                            author_icon=zunda, thumbnail=zunda,
                                                                            ))
                            first = True
                        prev_check = check
                        break
            await ctx.send(embed=await diyembed.getembed(self, color=0x1084fd, 
                                                                      description=result[3500 * (i + 1) + check:],
                                                                      footer_text="Pasted by Satt", footer_icon=zunda))
        return raw_result
    
    @commands.command()
    async def search(self, ctx, query=''):
        query = query.lower()
        raw_result = [s for s in voices if query in s]
        return await self.fetch(ctx, query=query, raw_result=raw_result)
    
    @commands.command()
    async def csearch(self, ctx, query=''):
        query = query.lower()
        raw_result = [s for s in cvoices if query in s]
        return await self.fetch(ctx, query=query, raw_result=raw_result)
    
    @commands.command()
    async def rawsearch(self, ctx, query=''):
        await ctx.reply(await self.search(ctx, query=query))

    @commands.command()
    async def crawsearch(self, ctx, query=''):
        await ctx.reply(await self.csearch(ctx, query=query))

    @commands.command()
    async def skip(self, ctx, query):
        try:
            await ctx.reply(f"Succesfully skipped {music_queue.pop(int(query) - 1)}!")
            await self.getq(ctx)
        except IndexError:
            await ctx.reply('Invalid index!')
        
    @commands.command()
    async def loop(self, ctx):
        """omg! loop feature"""
        global loop
        loop = False
        await ctx.reply('aight bro its gonna stop as soon as this track ends')
    
    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.reply('Player done!')
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        global music_queue
        music_queue = []
        print(music_queue)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))