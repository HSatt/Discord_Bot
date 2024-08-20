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
# target list
fucked = []

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
    
    @commands.command(
        name="mass_mention", # コマンドの名前。設定しない場合は関数名
        aliases=["mass", "mass_murder"], # ?hiでも ?heyでも反応するようになる
        description="targetを10回mentionするだけです"
    )
    async def mass_mention(self, ctx, target):
        for i in range(10):
            msg = await ctx.send(f'Fuck Off <@{target}>')
            fucked.append(msg.id)
        print(fucked)

    @commands.command(
        name="sorry", # コマンドの名前。設定しない場合は関数名
        aliases=[";;", "forgiveme", "gomen", "soy", "so-ri-", "sry"], # ?hiでも ?heyでも反応するようになる
        description="targetを10回mentionするだけです"
    )
    async def sorry(self, ctx):
        while fucked != []:
            for delete in fucked:
                try:
                    # メッセージIDを使ってメッセージオブジェクトを取得
                    message = await ctx.channel.fetch_message(delete)
                    await message.delete()
                    await ctx.send(f'Message with ID {delete} has been deleted.', delete_after=5)
                    fucked.remove(delete)
                except discord.NotFound:
                    await print('Message not found.')
                    return
                except discord.Forbidden:
                    await print('I do not have permission to delete this message.')
                    return
                except discord.HTTPException:
                    await print('Failed to delete message.')
                    return
                finally:
                    await asyncio.sleep(0.1)
        print(fucked)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if 'ストーリー読め' in message.content:
            await message.channel.send('# ブルーアーカイブのストーリーを読みましょう‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️')

async def setup(bot: commands.Bot):
    await bot.add_cog(fuck(bot))