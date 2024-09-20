import discord
from discord.ext import commands
from discord.ui import Button, View
import random
from atproto import Client # type: ignore
import time
import asyncio
from pyngrok import ngrok
from ytnoti import AsyncYouTubeNotifier, Video
import json
from httpx import InvalidURL
import requests
from bs4 import BeautifulSoup
from cogs.utils.diyembed import diyembed
from cogs.utils.nosj import nosj
from cogs.schedule import schedule
import re
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
import datetime
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
    
        youtube.notifier = AsyncYouTubeNotifier()

        @self.notifier.upload()
        async def listener(video: Video):
            print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] \033[1m !!New Post Detected!! \033[0m')
            print(video)
            channels = nosj.load("data/Server/channels.json")
            response = requests.get(video.url)
            soup = BeautifulSoup(response.text, features="lxml")
            try:
                youtube_str = soup.find("script", string=re.compile("scheduledStartTime")).get_text().replace("var ytInitialPlayerResponse = ", "")
                youtube_list = youtube_str.split('"')
                for item in youtube_list:
                    if "scheduledStartTime" in item:
                        start_time = youtube_list[youtube_list.index(item) + 2]
                        print(f"Live starting at {datetime.datetime.fromtimestamp(int(start_time))}")
                        start_time = datetime.datetime.fromtimestamp(int(start_time)) - timedelta(minutes=5)
                        break
            except AttributeError:
                start_time = None
                return
            for guild_id, channel_id in channels.items():
                guild_followed = nosj.load(f"data/Server/youtube_followed/{guild_id}.json")
                for followed in guild_followed:
                    if followed == video.channel.id:
                        channel = self.bot.get_channel(channel_id)
                        await channel.send(f"New video from {video.channel.name}: {video.title}({video.url})")
                        if start_time is not None:
                            scheduler = AsyncIOScheduler()
                            scheduler.add_job(self.starting_notification, 'date', run_date=start_time, args=[video.channel.name, video.title, video.url, channel_id])
                            scheduler.start()
                            print(f"Starting notification for {video.channel.name} @ {start_time}")

    async def starting_notification(self, channel_name, video_title, video_url, channel_id):
        print(f"Sending notification for {channel_name} @ {datetime.datetime.now()}")
        channel = self.bot.get_channel(int(channel_id))
        await channel.send(embed=await diyembed.getembed(title=f"{channel_name} is going live!",
                                                         title_url=video_url,
                                                         description=f"{video_title} is starting now!",
                                                         color=0xff0000))

    # 起動時
    @commands.Cog.listener()
    async def on_ready(self):
        for channel in subscribed:
            await self.notifier.subscribe(channel)  # Channel ID of Satt
        await self.notifier.serve() # Youtube君をスクレイピングする(ガチ)

    # subscribeコマンド
    @commands.command()
    async def sub(self, ctx, channel_id: str):
        try:
            await youtube.notifier.subscribe(channel_id)
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