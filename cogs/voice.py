import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View
from cogs.diyembed import diyembed
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp3 import HeaderNotFoundError
import json
import math
import asyncio
import os
import random

# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'
# 9
queue = []
#search待ち
wait_search = asyncio.Event()
# 回るレコード
disc = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2VwYm44ODhvcWcwc3g5ZHpkN3dnYjZ3eW00Y2dycDR6cXA2eTIwdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/uEwUiCNmNP6ATa1c7P/giphy.gif"
# channel
Manage_Channel = 1273134816308625439
# paths
path = "data/sounds"
cpath = "C://Users/hatos/Music"
npath = "./data/sana"
# buttons
class MyView(View):
    def __init__(self, ctx, query):
        super().__init__()
        self.ctx = ctx
        self.query = query

    @discord.ui.button(label="Musicフォルダ", style=discord.ButtonStyle.primary)
    async def music_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Musicフォルダ内で検索します…", ephemeral=True)
        with open(f"data/voice/lib/music.json", "r", encoding="utf-8") as f:
            voices = json.load(f)
        await voice.fetch(self, self.ctx, voices=voices, query=self.query, pre_path=cpath)

    @discord.ui.button(label="Soundライブラリ", style=discord.ButtonStyle.primary)
    async def sound_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Soundライブラリ内で検索します…", ephemeral=True)
        with open(f"data/voice/lib/sound.json", "r", encoding="utf-8") as f:
            voices = json.load(f)
        await voice.fetch(self, self.ctx, voices=voices, query=self.query, pre_path=path)

    @discord.ui.button(label="さなボタン", style=discord.ButtonStyle.primary)
    async def sana_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("さなボタン内で検索します…", ephemeral=True)
        with open(f"data/voice/lib/sana.json", "r", encoding="utf-8") as f:
            voices = json.load(f)
        await voice.fetch(self, self.ctx, voices=voices, query=self.query, pre_path=npath)

    @discord.ui.button(label="中止", style=discord.ButtonStyle.danger)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("中止します…", ephemeral=True)
        raw_result = []
        with open(f"data/voice/result/search.json", "w+", encoding="utf-8") as f:
            json.dump(raw_result, f)
        wait_search.set()

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx):
        await self.rel()
        await ctx.reply('Reloaded!')

    async def rel(self):
        global path
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
        with open(f"data/voice/lib/sound.json", "w+", encoding="utf-8") as f:
            json.dump(voices, f)
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
        with open(f"data/voice/lib/music.json", "w+", encoding="utf-8") as f:
            json.dump(cvoices, f)

        ndirs = [f for f in os.listdir(npath) if os.path.isdir(npath + "/" + f)]
        nvoices = []
        for dir in ndirs:
            if dir == "venv":
                continue
            files = os.listdir(npath + "/" + dir)
            for file in files:
                file_path = str(dir + "/" + file).lower()
                nvoices.append(file_path)
        with open(f"data/voice/lib/sana.json", "w+", encoding="utf-8") as f:
            json.dump(nvoices, f)


    async def join(self, ctx: Context):
        if not ctx.message.author.voice:
            await ctx.send(f"You are not connected to a voice channel")
            return
        else:
            channel = ctx.message.author.voice.channel
            try:
                await channel.connect()
            except Exception as e:
                print(e)
                pass
    
    @commands.command()
    async def call(self, ctx):
        await self.join(ctx)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("Data/sounds/soundboard/カードが必要なら.wav"))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

    @commands.command()
    async def stop(self, ctx):
        await ctx.reply('👋🏻')
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        global queue
        queue = []
        with open(f"data/voice/np/{self.bot.user.id}.json", "w+", encoding="utf-8") as f:
            json.dump("", f)
        
    async def length(self, query):
        try:
            if query.endswith('.mp3'):
                audio = MP3(query)
            elif query.endswith('.flac'):
                audio = FLAC(query)
            else:
                return 0
            return audio.info.length
        except FileNotFoundError:
            print(f"File not found: {query}")
            return 0
        except HeaderNotFoundError:
            print(f"Error loading audio file: {query}")
            return 0
        
    @commands.command(
        aliases=['p']
    )
    async def play(self, ctx, query="", player_loop=False):
        """Plays a file from the local filesystem"""
        await self.search(ctx, query)
        await wait_search.wait()
        wait_search.clear()
        print("Search done!")
        with open(f"data/voice/result/search.json", "r", encoding="utf-8") as f:
            result = json.load(f)
        if not result:
            await ctx.reply(embed=await diyembed.getembed(self, color=0x1084fd, 
                                                    description=f"検索結果が見つからなかったか、検索が中止されました。", 
                                                    author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                    author_icon=zunda, thumbnail=zunda, footer_text="Pasted by Satt", footer_icon=zunda
                                                    ))
        else:
            await voice.join(self, ctx)
            for content in result:
                queue.append(content)
                if not ctx.voice_client.is_playing():
                    await self.player(ctx, current=0, loop=player_loop)

    async def player(self, ctx, current, loop=False):
        try:
            print(queue[0])
        except IndexError:
            await ctx.send('No more songs in queue!')
            await voice.stop(self, ctx)
            return
        source = queue.pop(0)
        if loop == True:
            queue.append(source)
        with open(f"data/voice/np/{self.bot.user.id}.json", "w+", encoding="utf-8") as f:
            json.dump(source, f)
        if source.startswith("C://"):
            path_len = len(cpath)
        elif source.startswith("data/"):
            path_len = len(path)
        else:
            path_len = len(npath)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=source.split('/')[-1].title()))
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source))
        ctx.voice_client.play(source, 
                              after=lambda e: print(f'Player error: {e}') if e else self.bot.loop.create_task(voice.player(self, ctx, current=current, loop=loop)))
        
    @commands.command()
    async def search(self, ctx, query=''):
        view = MyView(ctx, query)
        return await ctx.reply(view=view, embed=await diyembed.getembed(self, title=f"""どのライブラリで"{query}"を検索しますか？""", color=0x1084fd,))

    async def fetch(self, ctx, voices, query='', pre_path=''):
        query = query.lower()
        raw_result = [s for s in voices if query in s]
        removed = []
        for item in raw_result:
            if item.endswith(".jpg") or item.endswith(".png") or item.endswith(".jpeg"):
                print(f"Thumbnail detected! {item}")
                removed.append(item)
        for removeitem in removed:
            raw_result.remove(removeitem)
        result = ''
        if raw_result == []:
            await ctx.reply('No results found!')
            return raw_result
        print(raw_result)
        result += f'📁 {raw_result[0].split('/')[0]}\n'
        prev_dir = raw_result[0].split('/')[0]
        for directory in raw_result:
            if prev_dir != directory.split('/')[0]:
                result += "📁 " + directory.split('/')[0] + "\n"
                prev_dir = directory.split('/')[0]
            if not "." in directory.split('/')[1]:
                count = 1
                print(directory.split('/'))
                while True:
                    for test in directory.split('/'):
                        if not test in result:
                            result += f'**' + 'ᅠ' * (count) + '┗**'
                            if not "." in test:
                                result += "📁 "
                            result += f'{test}\n'
                            if "." in test:
                                break
                        count += 1
                    break

            else:
                result += f'**┗**{directory.split('/')[1]}\n'
        
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
        for item in raw_result:
            raw_result[raw_result.index(item)] = pre_path + "/" + item
        with open(f"data/voice/result/search.json", "w+", encoding="utf-8") as f:
            json.dump(raw_result, f)
        wait_search.set()
        print(raw_result)
        return raw_result

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx):
        with open(f"data/voice/np/{self.bot.user.id}.json", "r", encoding="utf-8") as f:
            now_playing = json.load(f)
        if now_playing.startswith("C://"):
            path_len = len(cpath)
        elif now_playing.startswith("data/"):
            path_len = len(path)
        else:
            path_len = len(npath)
        try:
            if ctx.voice_client.is_playing():
                await ctx.send(embed=await diyembed.getembed(self, title=f"""再生中…""", color=0x1084fd, 
                                                        description=f"{now_playing[path_len:]}, {round(await voice.length(self, query=str(now_playing)), 3)}s", 
                                                        author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                        author_icon=zunda, thumbnail=disc,
                                                        ))
        except AttributeError:
            await ctx.send(embed=await diyembed.getembed(self, color=0x1084fd, 
                                                    title=f"何も再生されていません。", 
                                                    author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                    author_icon=zunda, thumbnail=disc, footer_text="Pasted by Satt", footer_icon=zunda
                                                    ))
            return
    
    @commands.command()
    async def skip(self, ctx, query):
        try:
            await ctx.reply(f"Succesfully skipped {queue.pop(int(query) - 1)}!")
            await self.getq(ctx)
        except IndexError:
            await ctx.reply('Invalid index!')

    async def pathlen(self, query):
        if query.startswith("C://"):
            path_len = len(cpath)
        elif query.startswith("data/"):
            path_len = len(path)
        else:
            path_len = len(npath)
        return path_len

    @commands.command()
    async def getq(self, ctx):
        reciept = ''
        with open(f"data/voice/np/{self.bot.user.id}.json", "r", encoding="utf-8") as f:
            now_playing = json.load(f)
            path_len = await self.pathlen(now_playing)
            reciept += f'**Now Playing**: {now_playing[path_len:]}\n'
        for raw_item in queue:
            path_len = await self.pathlen(raw_item)
            reciept += f'- {raw_item[path_len:]}\n'
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
    async def shuffle(self, ctx):
        random.shuffle(queue)
        await ctx.reply('Queue shuffled!')
        await self.getq(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.rel(self)

async def setup(bot):
    await bot.add_cog(voice(bot))