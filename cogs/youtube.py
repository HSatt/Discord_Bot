import discord
from discord.ext import commands
from discord.ui import Button, View
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
from cogs.diyembed import diyembed
from cogs.bluesky import bluesky
from cogs.tweet import tweet

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

# buttons
class Follow_Bridge(View):
    def __init__(self, ctx, target_id):
        super().__init__()
        self.ctx = ctx
        self.target_id = target_id

    @discord.ui.button(emoji="<:youtube:1284353556836778024>", label="Bluesky", style=discord.ButtonStyle.primary)
    async def bsky_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Bluesky上の{self.target_id}をフォローします…", ephemeral=True)
        await bluesky.bfollow(self, self.ctx, self.target_id)
    
    @discord.ui.button(label="Twitter", style=discord.ButtonStyle.primary)
    async def twitter_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Twitter上の{self.target_id}をフォローします…", ephemeral=True)
        await tweet.follow(self, self.ctx, self.target_id)

    @discord.ui.button(label="Youtube", style=discord.ButtonStyle.primary)
    async def youtube_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Youtube上の{self.target_id}をフォローします…", ephemeral=True)
        self.target_id = await youtube.convert(self, self.ctx, self.target_id)
        await youtube.sub(self, self.ctx, self.target_id)

# MAKE IT COGGY
class youtube(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
        youtube.notifier = AsyncYouTubeNotifier()

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

    # followsコマンド
    @commands.command()
    async def follows(self, ctx, target_id):
        view = Follow_Bridge(ctx, target_id)
        await ctx.reply(view=view, embed=await diyembed.getembed(self, title=f"""どのプラットフォームで"{target_id}"をフォローしますか？""", color=0x1084fd,))
    
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