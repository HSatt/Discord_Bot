import discord
from discord.ext import commands
import random
import datetime
from atproto import Client # type: ignore
import time
import asyncio
from pyngrok import ngrok
from ytnoti import AsyncYouTubeNotifier, Video

# チャンネル指定
Manage_Channel = 1273134816308625439

# MAKE IT COGGY
class fuck(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # fuckコマンドの定義
    @commands.command(
        name="fuck", # コマンドの名前。設定しない場合は関数名
        aliases=["hi", "hey"] # ?hiでも ?heyでも反応するようになる
    )
    async def fuck(self, ctx):
        await ctx.reply(f'Fuck Off {ctx.author.mention}')

async def setup(bot: commands.Bot):
    await bot.add_cog(fuck(bot))