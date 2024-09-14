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
from httpx import InvalidURL
import requests
from bs4 import BeautifulSoup

# チャンネル指定
Manage_Channel = 1273134816308625439

# Youtubeから通知を持ってくる
ngrok_token = ''
with open("data/!important/ngrok_token.json", "r", encoding="utf-8") as f:
    ngrok_token = json.load(f)
ngrok.set_auth_token(ngrok_token)

# give me sub list :handgun:
subscribed = []
with open("data/subscribed.json", "r", encoding="utf-8") as f:
    subscribed = json.load(f)
print(subscribed)

# MAKE IT COGGY
class youtube(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
        self.notifier = AsyncYouTubeNotifier()

        @self.notifier.upload()
        async def listener(video: Video):
            print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] \033[1m !!New Post Detected!! \033[0m')
            print(video)
            channel = self.bot.get_channel(Manage_Channel)
            await channel.send(f"New video from {video.channel.name}: {video.title}({video.url})")

    # 起動時
    @commands.Cog.listener()
    async def on_ready(self):
        global bsky_embed
        for channel in subscribed:
            await self.notifier.subscribe(channel)  # Channel ID of Satt
        await self.notifier.serve() # Youtube君をスクレイピングする(ガチ)
    
    # subscribeコマンド
    @commands.command(
        name="subscribe", # コマンドの名前。設定しない場合は関数名
        aliases=["sub"]
    )
    async def subscribe(self, ctx, channel_id: str):
        try:
            await AsyncYouTubeNotifier.subscribe(self=self, channel_ids=channel_id)
            subscribed.append(channel_id)
            await ctx.reply(f'Succesfully subscribed {channel_id}!')
            with open("data/subscribed.json", "w+", encoding="utf-8") as f:
                json.dump(subscribed, f)
        except ValueError:
            await ctx.reply(f"Invalid channel ID: {channel_id}")
            return
        except InvalidURL:
            await ctx.reply(':middle_finger:')

    @commands.command(
        name="convert", # コマンドの名前。設定しない場合は関数名
        aliases=["con"]
    )
    async def convert(self, ctx, handle: str):
        try:
            resp = requests.get(f'https://www.youtube.com/@{handle}')
            soup = BeautifulSoup(resp.text, features="lxml")
            link = soup.select_one('link[rel="canonical"]')
            if link is None:
                print("Failed to fetch channel id.")
                await ctx.reply("Failed to fetch channel id.")
            else:
                id = link["href"].split("/")[-1]
                print(id, end="")
                await ctx.reply(f'id: {id}')
                return id
        except Exception as e:
            print(e)
            await ctx.reply(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(youtube(bot))