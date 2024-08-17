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
class delete(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # deleteコマンドの定義
    @commands.command()
    async def delete(self, ctx, message_id: int):
        try:
            # メッセージIDを使ってメッセージオブジェクトを取得
            message = await ctx.channel.fetch_message(message_id)
            await message.delete()
            await ctx.send(f'Message with ID {message_id} has been deleted.', delete_after=5)
        except discord.NotFound:
            await ctx.send('Message not found.', delete_after=5)
        except discord.Forbidden:
            await ctx.send('I do not have permission to delete this message.', delete_after=5)
        except discord.HTTPException:
            await ctx.send('Failed to delete message.', delete_after=5)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(delete(bot))