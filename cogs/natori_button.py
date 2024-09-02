import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
import random
from cogs.diyembed import diyembed
from cogs.remusic import Music
import math
from mutagen.mp3 import MP3
now_playing = ''
path = "./data/sana"
dirs = [f for f in os.listdir(path) if os.path.isdir(path + "/" + f)]
voices = []
natori_queue = []
# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'

for dir in dirs:
    if dir == "venv":
        continue
    files = os.listdir(path + "/" + dir)
    for file in files:
        file_path = str(dir + "/" + file).lower()
        voices.append(file_path)

# MAKE IT COGGY
class natori_button(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def natoriloop(self, ctx: Context) -> None:
        voice_path = random.choice(voices)
        ctx.voice_client.play(
            discord.FFmpegPCMAudio(voice_path), after=lambda e: self.natoriloop(ctx)
        )

    @commands.command(
        name="natoriplay", # コマンドの名前。設定しない場合は関数名
        aliases=['playnatori', 'nplay', 'pnatori', 'nsound']
    )
    async def natoriplay(self, ctx, query=''):
        query = await self.nsearch(ctx, query)
        print(query)
        await Music.join(self, ctx)
        for content in query:
            content = path + "/" + content
            natori_queue.append(content)
            if not ctx.voice_client.is_playing():
                await self.nplayer(ctx, current=0)

    async def nplayer(self, ctx, current, loop=False):
        if loop == True:
            try:
                print(natori_queue[current])
            except IndexError:
                current = 0
                print(natori_queue[current])
            source = natori_queue[current]
            current += 1
        else:
            try:
                print(natori_queue[0])
            except IndexError:
                await ctx.reply('No more songs in queue!')
                await Music.stop(self, ctx)
                return
            source = natori_queue.pop(0)
            global now_playing
            now_playing = source
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source))
        ctx.voice_client.play(source, 
                              after=lambda e: print(f'Player error: {e}') if e else self.bot.loop.create_task(self.nplayer(ctx, current=current)))
        
    @commands.command()
    async def inf(self, ctx: Context) -> None:
        print("a")
        if ctx.author.voice is None:
            await ctx.reply("vc はいらんかい")

        if ctx.voice_client is not None:
            if ctx.voice_client.is_playing():
                await ctx.reply("今話してっから待ちなさい！")
                return

        try:
            await ctx.author.voice.channel.connect()
        except Exception as e:
            print(e)

        self.natoriloop(ctx)

    @commands.command()
    async def nsearch(self, ctx, query=''):
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
        prev_result = raw_result[0].split('/')[0]
        result += f'{raw_result[0].split('/')[0]}\n'
        for directory in raw_result:
            if directory.split('/')[0] != prev_result:
                result += f'{directory.split('/')[0]}\n'
                prev_result = directory.split('/')[0]
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
        print(raw_result)
        return raw_result

    @commands.command()
    async def ngetq(self, ctx):
        reciept = ''
        for raw_item in natori_queue:
            getq_response = ''
            for thing in raw_item.split('/'):
                if not thing in path:
                    getq_response += thing + '/'
            reciept += f'- {getq_response}\n'
        if len(reciept) <= 6000:
            await ctx.reply(embed=await diyembed.getembed(self, title="Queue", color=0x1084fd, description=f"{reciept}",))
        else:
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
                            await ctx.send(embed=await diyembed.getembed(self, title=f"""Queue""", color=0x1084fd, 
                                                                            description=reciept[:3500 + check], 
                                                                            author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                                            author_icon=zunda, thumbnail=zunda,
                                                                            ))
                            first = True
                        prev_check = check
                        break
            await ctx.send(embed=await diyembed.getembed(self, color=0x1084fd, 
                                                                      description=reciept[3500 * (i + 1) + prev_check:],
                                                                      footer_text="Pasted by Satt", footer_icon=zunda))
    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx):
        try:
            file = discord.File(now_playing)
            await ctx.send(file=file, embed=await diyembed.getembed(self, title=f"""Now Playing...""", color=0x1084fd, 
                                                    description=f"{now_playing}, {round(await self.length(query=str(now_playing)), 3)}s", 
                                                    author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                    author_icon=zunda, thumbnail=zunda,
                                                    ))
        except FileNotFoundError:
            await ctx.reply('Not Playing!')
            return
        
    @commands.command()
    async def getme(self, ctx, query):
        try:
            query = path + "/" + query
            file = discord.File(query)
            await ctx.send(file=file, embed=await diyembed.getembed(self, title=f"""Here you go.""", color=0x1084fd, 
                                                    description=f"{query}, {round(await self.length(query=str(query)), 3)}s", 
                                                    author_name='Soundboard bot for poors', author_url='https://satt.carrd.co/', 
                                                    author_icon=zunda, thumbnail=zunda,
                                                    ))
        except FileNotFoundError:
            await ctx.reply('File not found!')
            return
        
    async def length(self, query):
        """get length"""
        audio = MP3(query)
        return audio.info.length
    
    @commands.command()
    async def nshuffle(self, ctx):
        random.shuffle(natori_queue)
        await ctx.reply('Queue shuffled!')
        await self.ngetq(ctx)

    @commands.command()
    async def ping(self, ctx: Context) -> None:
        await ctx.reply("pong")

async def setup(bot: commands.Bot):

    await bot.add_cog(natori_button(bot))