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
table = {'😔': 5, '🤮': 15, '😡': 30, '🥲': 45, '😋': 80, '🐢': 1341141758683892.75}
# zunda mochi
zunda = 'https://i.imgur.com/6bgRNLR.png'
global bank_info
bank_info = {}
with open("data/bank_info.json", "r", encoding="utf-8") as f:
# bank_info.jsonを開く(r)
    bank_info = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
print('Successfully loaded previous bank_info record!')

# MAKE IT COGGY
class gamble(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # gambleコマンドの定義
    @commands.command(
        name="gamble", # コマンドの名前。設定しない場合は関数名
        aliases=["money", "cash"] # ?moneyでも ?cashでも反応するようになる
    )
    async def gamble(self, ctx):
        global bank_info
        self.gain = random.randrange(-10, 10)
        try:
            print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] {ctx.author.name} has gained {self.gain} coin(s)!')
            bank_info[str(ctx.author.id)] += self.gain
        except KeyError:
            bank_info[str(ctx.author.id)] = 100 + self.gain
            return
        finally:
            embed = self.bot.get_command("embed")
            await embed(ctx, title="You rolled a dice...", description=f'''And you've got **{self.gain}** coins!''', author_name='Gamble Addiction',
                        author_url='https://satt.carrd.co/', author_icon=zunda, thumbnail='', image='', 
                        field1_name='You now have:', field1_value=f'🪙 {bank_info[str(ctx.author.id)]} coins!', 
                        field2_name='', field2_value='', footer_text="Pasted by Satt", footer_icon=zunda)
            with open("data/bank_info.json", "w+", encoding="utf-8") as f:
                json.dump(bank_info, f)
    
    # bankコマンドの定義
    @commands.command(
        name="bank", # コマンドの名前。設定しない場合は関数名
        aliases=["purse"]
    )
    async def bank(self, ctx):
        try:
            await ctx.reply(f'You have {bank_info[str(ctx.author.id)]} coins')
        except KeyError:
            await ctx.reply('Fuck you. Open bank first by doing *cash')
        
    # helpコマンドの定義
    @commands.command(
        name="helpmeplease;;", # コマンドの名前。設定しない場合は関数名
        aliases=["ineedhelp"]
    )
    async def helpmeplease(self, ctx):
        try:
            bank_info[str(ctx.author.id)] += 100
            await ctx.reply(f'Fine, now you have {bank_info[str(ctx.author.id)]} coins.')
            with open("data/bank_info.json", "w+", encoding="utf-8") as f:
                json.dump(bank_info, f)
        except KeyError:
            await ctx.reply('Fuck you. Open bank first by doing *cash')
    
    # slotコマンドの定義
    @commands.command(
        name="slot", # コマンドの名前。設定しない場合は関数名
    )
    async def slot(self, ctx):
        try:
            if bank_info[str(ctx.author.id)] <= 0:
                await ctx.reply('bye bye broke boy')
            else:
                result = ''
                bank_info[str(ctx.author.id)] -= 1
                for i in range(3):
                    result += f'**|**{emojis[random.randrange(6)]}'
                result += '**|**'
                if result[1] == result[3] == result[5]:
                    for face, reward in table.items():
                        if result[1] == face:
                            bank_info[str(ctx.author.id)] += reward
                            print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] {ctx.author.name} has gained {reward} coin(s)!')                 
                            await ctx.reply(f'You gained {reward} coins fr, Now you have {bank_info[str(ctx.author.id)]} coins 🤓')
                embed = self.bot.get_command("embed")
                await embed(ctx, title='You used a coin and pulled the lever...', description=result, author_name='Gamble Addiction', author_url='https://satt.carrd.co/',
                            author_icon=zunda, thumbnail='', image='', field1_name='You now have:', field1_value=f'🪙 {bank_info[str(ctx.author.id)]} coins!', 
                            field2_name='', field2_value='', footer_text="Pasted by Satt", footer_icon=zunda)
                with open("data/bank_info.json", "w+", encoding="utf-8") as f:
                    json.dump(bank_info, f)
        except KeyError:
            bank_info[str(ctx.author.id)] = 100   
        

    

async def setup(bot: commands.Bot):
    await bot.add_cog(gamble(bot))