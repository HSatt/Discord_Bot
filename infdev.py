import discord
from discord.ext import commands
import random
import datetime
from atproto import Client # type: ignore
import time
import asyncio
from pyngrok import ngrok
from ytnoti import AsyncYouTubeNotifier, Video
from cogs import getnatori, fuck, delete, gamble, youtube, tweet
import json

initial_extensions = (
    "cogs.getnatori", 
    "cogs.fuck",
    "cogs.delete",
    "cogs.gamble",
    "cogs.youtube",
    "cogs.tweet",
)

description = '''Hello.

There are a number of utility commands being showcased here.'''

# チャンネル指定
Manage_Channel = 1273134816308625439

# ずんだもん
zunda = "https://cdn.discordapp.com/emojis/1183011525947047957.png&quality=lossless"

# Blueskyから情報を持ってくる
bsky_client = Client("https://api.bsky.app") # botに入れるならbsky_clientとかのほうがわかりやすいかも - おけ！

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='*', description=description, intents=intents) # ここにcommands.Botで使ってたパラメータを入れる
    
    async def setup_hook(self) -> None: # ログインする前に実行されるイベント
        await bot.load_extension("jishaku")
        for extension in initial_extensions: 
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(e)
                print(f"Failed to load extension {extension}.")
            
bot = MyBot()
bot_token = ''
with open("data/!important/bot_token.json", "r", encoding="utf-8") as f:
    bot_token = json.load(f)

bot.run(bot_token)
