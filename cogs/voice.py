import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View
from cogs.utils.diyembed import diyembed
from mutagen.mp3 import MP3
from mutagen.flac import FLAC, FLACNoHeaderError
from mutagen.mp3 import HeaderNotFoundError
from mutagen.id3 import ID3NoHeaderError
import json
import math
import asyncio
import os
import random
import requests
from cogs.utils.nosj import nosj
from bs4 import BeautifulSoup
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageSequence, ImageDraw
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

# 回るレコードを作る(thanks qono)
def get_disc():
    disc_gif = Image.open("data/disc.gif")
    thumbnail = Image.open("data/thumbnail.jpg").convert("RGBA").resize((220, 220))
    mask = Image.open("data/disc_mask.png").convert("RGBA")

    center_x = disc_gif.width // 2
    center_y = disc_gif.height // 2

    rotate_per_frame = -360 / 81  # nice hard code!!

    frames = []
    for i, frame in enumerate(ImageSequence.Iterator(disc_gif)):
        frame_rgba = frame.convert("RGBA")

        # 画像サイズが違うと怒られるので別のImageに貼り付ける
        thumb_canvas = Image.new("RGBA", disc_gif.size)
        thumb = thumbnail.copy().rotate(rotate_per_frame * i)

        # 中心からThumbの位置をthumb/2分引いて、中心に合わせている
        x = round(center_x - (thumb.width / 2))
        y = round(center_y - (thumb.height / 2))
        thumb_canvas.paste(thumb, (x, y))
        masked = Image.composite(thumb_canvas, frame_rgba, mask)
        draw = ImageDraw.Draw(masked)
        draw.ellipse((disc_gif.height / 2 - 13, disc_gif.width / 2 - 13, disc_gif.height / 2 + 12, disc_gif.width / 2 + 12), fill=(0, 0, 0))
        frames.append(masked)

    # ここはネットから拾ったので何も分かりません
    frames[0].save(
        "data/disc_w_cover.gif",
        save_all=True,
        append_images=frames[1:],
        duration=disc_gif.info["duration"],
        loop=0,
    )
    return "data/disc_w_cover.gif"

google_token = nosj.load("data/!important/google_token.json")
async def fetch_lyric(ctx, query):
    params = {"key": google_token,
          "cx": "b56b70970672e45f2",
          "q": query,
          "gl": "ja",
          "hl": "ja"
          }

    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    soup = BeautifulSoup(response.text, features="lxml")
    text = response.text
    data = json.loads(text)
    print(soup)
    url = ""
    try:
        for item in data['items']:
            print(item['title'])
            if query in item['title']:
                url = item['link']
                thumbnail = item['pagemap']['cse_image'][0]['src']
                break
        if url == "":
            raise KeyError
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="lxml")
        lyrics = str(soup.select_one("#PriLyr")).split("\n")
        print(lyrics)
        if lyrics == ['None']:
            raise KeyError
        result = ""
        for lyric in lyrics:
            if lyric == '<div class="olyrictext" id="PriLyr">':
                lyric = ""
                pass
            if '<p>' in lyric or '</p>'in lyric or '</div>' in lyric or '<div id="amplified_100005381"><p id="widgetLoaded">' in lyric:
                lyric = lyric.replace("<p>", "").replace("</p>", "").replace("</div>", "").replace('<div id="amplified_100005381"><p id="widgetLoaded">', "")
            if "<br/>" in lyric:
                lyric = lyric.replace("<br/>", "\n").replace("<br/>", "\n")
            result += lyric
    except KeyError:
        await ctx.reply("No results found on lyrical-nonsense.com, trying on Genius.com...")
        bearer_token = nosj.load("data/!important/genius_token.json")

        headers = {"Authorization": f"Bearer {bearer_token}"}

        response = requests.get(f"https://api.genius.com/search?q={query}", headers=headers)
        try:
            for i in range(10):
                if query.lower() in response.json()["response"]["hits"][i]["result"]["full_title"].lower():
                    url = response.json()["response"]["hits"][i]["result"]["url"]
                    thumbnail = response.json()['response']['hits'][i]['result']['song_art_image_url']
                    break
        except IndexError:
            await ctx.reply("No results found!")
            return
        if not url:
            await ctx.reply("No results found!")
            return
        print(url)
        print(thumbnail)
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'lxml')
        lyrics = soup.select("#lyrics-root > div.Lyrics__Container-sc-1ynbvzw-1.kUgSbL")
        lyric_text = ""
        for lyric in lyrics:
            lyric_text += lyric.prettify()
        lyric_text = lyric_text.split("\n")
        result = ""
        red = False
        for item in lyric_text:
            if item in (" <i>", " </i>", '</div>', '', '<div class="Lyrics__Container-sc-1ynbvzw-1 kUgSbL" data-lyrics-container="true">', ):
                pass
            elif '<a class="ReferentFragmentdesktop' in item or '<span' in item or '</span>' in item or '</a>' in item:
                pass
            elif "<br/>" in item:
                result += "\n"
            elif "<b>" in item or "</b>" in item:
                if red != True:
                    red = True
                    result += "**"
                else:
                    pass
            else:
                result += item
                red = False
    try:
        await ctx.reply(embed=await diyembed.getembed(author_icon=zunda, author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/',
                                                      title=f"""「{query}」の歌詞""", title_url=url, description=f"""{result}""", color=0x1084fd,
                                                      thumbnail=thumbnail, footer_text="Pasted by Satt", footer_icon=zunda))
    except discord.HTTPException:
        await ctx.reply(f"うわーん！リストが長すぎます！ このレシートは{len(result)}mです！")

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

class get_lyric(View):
    def __init__(self, ctx, query):
        super().__init__()
        self.ctx = ctx
        self.query = query

    @discord.ui.button(label="歌詞", style=discord.ButtonStyle.primary)
    async def lyric_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("歌詞を取得します…", ephemeral=True)
        await fetch_lyric(ctx=self.ctx, query=self.query)


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
        await self.bot.change_presence(activity=None)
        
    async def length(self, query):
        try:
            if query.endswith('.mp3'):
                audio = MP3(query)
            elif query.endswith('.flac'):
                audio = FLAC(query)
            else:
                return 0
            return f"{f"{int(audio.info.length // 60)} min {round(audio.info.length % 60, 2)} sec" if audio.info.length > 60 else f"{round(audio.info.length, 2)} sec" }"
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
            await ctx.reply(embed=await diyembed.getembed(color=0x1084fd, 
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
        self.get_thumbnail(source)
        get_disc()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.get_elems(source)["title"]} by {self.get_elems(source)['artist']}"))
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source))
        ctx.voice_client.play(source, 
                              after=lambda e: print(f'Player error: {e}') if e else self.bot.loop.create_task(voice.player(self, ctx, current=current, loop=loop)))
        
    @commands.command()
    async def search(self, ctx, query=''):
        view = MyView(ctx, query)
        return await ctx.reply(view=view, embed=await diyembed.getembed(title=f"""どのライブラリで"{query}"を検索しますか？""", color=0x1084fd,))

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
            await ctx.reply(embed=await diyembed.getembed(title=f"""You searched for "{query}"...""", color=0x1084fd, description=result, 
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
                            await ctx.send(embed=await diyembed.getembed(color=0x1084fd,
                                                                         description=result[3500 * (i) + prev_check:3500 * (i + 1) + check],  
                                                                            ))
                        if first == False:
                            await ctx.send(embed=await diyembed.getembed(title=f"""You searched for "{query}"...""", color=0x1084fd, 
                                                                            description=result[:3500 + check], 
                                                                            author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                                            author_icon=zunda, thumbnail=zunda,
                                                                            ))
                            first = True
                        prev_check = check
                        break
            await ctx.send(embed=await diyembed.getembed(color=0x1084fd, 
                                                                      description=result[3500 * (i + 1) + check:],
                                                                      footer_text="Pasted by Satt", footer_icon=zunda))
        for item in raw_result:
            raw_result[raw_result.index(item)] = pre_path + "/" + item
        with open(f"data/voice/result/search.json", "w+", encoding="utf-8") as f:
            json.dump(raw_result, f)
        wait_search.set()
        print(raw_result)
        return raw_result
    
    @staticmethod
    def get_mp3_thumbnail(file_path):
        audio = MP3(file_path, ID3=ID3)
        try:
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    with open("data/thumbnail.jpg", "wb") as img:
                        img.write(tag.data)
                    return "data/thumbnail.jpg"
        except AttributeError:
            return None
    
    @staticmethod
    def get_flac_thumbnail(file_path):
        audio = FLAC(file_path)
        try:
            for picture in audio.pictures:
                with open("data/thumbnail.jpg", "wb") as img:
                    img.write(picture.data)
                return "data/thumbnail.jpg"
        except AttributeError:
            return None
    
    @staticmethod
    def get_mp3_elems(file_path):
        try:
            audio = MP3(file_path)
        except ID3NoHeaderError:
            return 
        mp3_elems = {}
        try:
            for title in audio["TIT2"]:
                mp3_elems["title"] = title
        except KeyError:
            mp3_elems["title"] = file_path.split('/')[-1].replace('.mp3', '').replace(".flac", "").split("_")[0]
        try:
            for artist in audio["TPE1"]:
                mp3_elems["artist"] = artist
        except KeyError:
            mp3_elems["artist"] = "Unknown Artist"
        try:
            for desc in audio["COMM"]:
                mp3_elems["desc"] = desc
        except KeyError:
            mp3_elems["desc"] = f"https://www.youtube.com/results?search_query={file_path.split('/')[-1].replace('.mp3', '').replace(" ", "+")}"
        return mp3_elems

    @staticmethod
    def get_flac_elems(file_path):
        try:
            audio = FLAC(file_path)
        except FLACNoHeaderError:
            return 
        flac_elems = {}
        try:
            for title in audio["title"]:
                flac_elems["title"] = title
        except KeyError:
            flac_elems["title"] = file_path.split('/')[-1].replace('.flac', '').replace(".mp3", "").split("_")[0]
        try:
            for artist in audio["artist"]:
                flac_elems["artist"] = artist
        except KeyError:
            flac_elems["artist"] = "Unknown Artist"
        try:
            for desc in audio["description"]:
                 flac_elems["desc"] = desc
        except KeyError:
            flac_elems["desc"] = f"https://www.youtube.com/results?search_query={file_path.split('/')[-1].replace('.flac', '').replace(" ", "+")}"
        return flac_elems
    
    @staticmethod
    def get_elems(query):
        # カバーアート情報取得
        if query.endswith(".flac") == True:
            elems = voice.get_flac_elems(file_path=query)
        elif query.endswith(".mp3") == True:
            elems = voice.get_mp3_elems(file_path=query)
        else:
            elems = None
        return elems
    
    @staticmethod
    def get_thumbnail(query):
        # カバーアート情報取得
        if query.endswith(".flac") == True:
            thumbnail_path = voice.get_flac_thumbnail(file_path=query)
        elif query.endswith(".mp3") == True:
            thumbnail_path = voice.get_mp3_thumbnail(file_path=query)
        else:
            thumbnail_path = None
        if thumbnail_path:
            print(f"サムネイルを保存しました: {thumbnail_path}")
            cover = Image.open(thumbnail_path)
            if cover.height / cover.width != 1:
                cropped = cover.crop(((cover.width - cover.height) / 2, 0, cover.width - (cover.width - cover.height) / 2, cover.height))
                cropped.save(thumbnail_path)
            return thumbnail_path
        else:
            print("サムネイルが見つかりませんでした。")
            return None

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx):
        with open(f"data/voice/np/{self.bot.user.id}.json", "r", encoding="utf-8") as f:
            now_playing = json.load(f)
        try:
            if ctx.voice_client.is_playing():
                sound_elems = self.get_elems(now_playing)
                view = get_lyric(ctx, query=sound_elems["title"])
                cover = discord.File("data/thumbnail.jpg", filename="temp.jpg")
                disc_cover = discord.File("data/disc_w_cover.gif", filename="disc.gif")
                await ctx.send(view=view, files=[cover if cover else None, disc_cover if disc_cover else None], embed=await diyembed.getembed(title=f"""▶️ 再生中…""", title_url=sound_elems["desc"], color=0x1084fd, 
                                                        description=f"{sound_elems['title']} by {sound_elems["artist"]}. \n {await voice.length(self, query=str(now_playing))} \n[[Youtube]({sound_elems['desc']})]", 
                                                        author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', image="attachment://temp.jpg",
                                                        author_icon=zunda, thumbnail="attachment://disc.gif", footer_text="Pasted by Satt", footer_icon=zunda
                                                        ))
        except Exception as e:
            print(e)
            await ctx.send(embed=await diyembed.getembed(color=0x1084fd, 
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
            await ctx.reply(embed=await diyembed.getembed(title="Queue", color=0x1084fd, description=f"{reciept}",))
        except discord.HTTPException:
            await ctx.reply(f"うわーん！リストが長すぎます！ このレシートは{len(reciept)}mです！")
            print(f"this result contains: {len(reciept)} characters")
            first = False
            for i in range(math.floor(len(reciept) / 3500)):
                for check in range(500):
                    if str(reciept[3500 * (i + 1) + check]) == str("-"):
                        check -= 1
                        if first == True:
                            await ctx.send(embed=await diyembed.getembed(color=0x1084fd,
                                                                         description=reciept[3500 * (i) + prev_check:3500 * (i + 1) + check],  
                                                                            ))
                        if first == False:
                            await ctx.send(embed=await diyembed.getembed(title=f"Queue", color=0x1084fd, 
                                                                            description=reciept[:3500 + check], 
                                                                            author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                                            author_icon=zunda, thumbnail=zunda,
                                                                            ))
                            first = True
                        prev_check = check
                        break
            await ctx.send(embed=await diyembed.getembed(color=0x1084fd, 
                                                                      description=reciept[3500 * (i + 1) + check:],
                                                                      footer_text="Pasted by Satt", footer_icon=zunda))
            
    @commands.command()
    async def shuffle(self, ctx):
        random.shuffle(queue)
        await ctx.reply('Queue shuffled!')
        await self.getq(ctx)

    @commands.command()
    async def lyric(self, ctx, *, query):
        await fetch_lyric(ctx, query)
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.rel()

async def setup(bot):
    await bot.add_cog(voice(bot))