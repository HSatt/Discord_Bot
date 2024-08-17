import discord
from discord.ext import commands
import random
import datetime
from atproto import Client # type: ignore
import time
import asyncio
from pyngrok import ngrok
from ytnoti import AsyncYouTubeNotifier, Video
import json

# チャンネル指定
Manage_Channel = 1273134816308625439

# emojis for slot
emojis = ['😋', '🤮', '😡', '😔', '🥲', '🐢']
global gain
gain = 0

# MAKE IT COGGY
class gamble(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # when launched
    @commands.Cog.listener()
    async def on_ready(self) -> None: # selfめっちゃ大事！！！！！！！！ 
        global bank
        bank = {}
        with open("data/bank.json", "r", encoding="utf-8") as f:
            # bank.jsonを開く(r)
            bank = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
            print('Successfully loaded previous bank record!')

    # gambleコマンドの定義
    @commands.command(
        name="gamble", # コマンドの名前。設定しない場合は関数名
        aliases=["money", "cash"] # ?moneyでも ?cashでも反応するようになる
    )
    async def gamble(self, ctx):
        gain = random.randrange(-10, 10)
        try:
            print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] {ctx.author.name} has gained {gain} coin(s)!')
            bank[str(ctx.author.id)] += gain
        except KeyError:
            bank[str(ctx.author.id)] = 100 + gain
            return
        finally:
            await ctx.reply(f'You gained {gain} coins fr, Now you have {bank[str(ctx.author.id)]} coins 🤓')
            with open("data/bank.json", "w+", encoding="utf-8") as f:
                json.dump(bank, f)
    
    # bankコマンドの定義
    @commands.command(
        name="bank", # コマンドの名前。設定しない場合は関数名
        aliases=["purse"]
    )
    async def bank(self, ctx):
        try:
            await ctx.reply(f'You have {bank[str(ctx.author.id)]} coins')
        except KeyError:
            await ctx.reply('Fuck you. Open bank dirst by doing *cash')
        
    # helpコマンドの定義
    @commands.command(
        name="helpmeplease;;", # コマンドの名前。設定しない場合は関数名
        aliases=["ineedhelp"]
    )
    async def helpmeplease(self, ctx):
        try:
            bank[str(ctx.author.id)] += 100
            await ctx.reply(f'Fine, now you have {bank[str(ctx.author.id)]} coins.')
            with open("data/bank.json", "w+", encoding="utf-8") as f:
                json.dump(bank, f)
        except KeyError:
            await ctx.reply('Fuck you. Open bank dirst by doing *cash')
    
    # slotコマンドの定義
    @commands.command(
        name="slot", # コマンドの名前。設定しない場合は関数名
    )
    async def slot(self, ctx):
        try:
            if bank[str(ctx.author.id)] <= 0:
                await ctx.reply('bye bye broke boy')
            else:
                result = ''
                gain = 0
                bank[str(ctx.author.id)] -= 5
                for i in range(3):
                    result += f'|{emojis[random.randrange(6)]}'
                result += '|'
                await ctx.reply(result)
                if result[1] == result[3] == result[5]:
                    if result[1] == '😔':
                        gain = 5
                    elif result[1] == '🤮':
                        gain = 15
                    elif result[1] == '😡':
                        gain = 30
                    elif result[1] == '🥲':
                        gain = 45
                    elif result[1] == '😋':
                        gain = 80
                    elif result[1] == '🐢':
                        gain = 1341141758683892.75
                    print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] {ctx.author.name} has gained {gain} coin(s)!')
                    bank[str(ctx.author.id)] += gain                    
                    await ctx.reply(f'You gained {gain} coins fr, Now you have {bank[str(ctx.author.id)]} coins 🤓')
                    with open("data/bank.json", "w+", encoding="utf-8") as f:
                        json.dump(bank, f)
        except KeyError:
            await ctx.reply('Fuck you. Open bank dirst by doing *cash')
            return
        finally:
            with open("data/bank.json", "w+", encoding="utf-8") as f:
                        json.dump(bank, f)

async def setup(bot: commands.Bot):
    await bot.add_cog(gamble(bot))