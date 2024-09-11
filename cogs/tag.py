import discord
from discord.ext import commands
import random
from atproto import Client # type: ignore
import asyncio
import json
from cogs.diyembed import diyembed

trigger = {}
with open("data/trigger.json", "r", encoding="utf-8") as f:
# bank_info.jsonを開く(r)
    trigger = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
print('Successfully loaded previous trigger record!')

class tag(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, mode, key, *, value=''):
        if mode == 'create':
            trigger[key] = value
            print(f'Succesfully created: {key} for {trigger[key]}!')
            try:
                await ctx.reply(f'Succesfully created: {key} for {trigger[key]}!')
            except discord.HTTPException:
                await ctx.reply('bros tag is longer than my pp :skull:')
        elif mode == 'remove':
            try:
                removed = trigger.pop(key)
                print(f'Succesfully removed: {key} for {removed}!')
                await ctx.reply(f'Succesfully removed: {key} for {removed}!')
            except KeyError:
                await ctx.reply('The key you entered does not exist in the list.')
                return
        else:
            await ctx.reply('You need to use either create or remove to use this command!')
        with open("data/trigger.json", "w+", encoding="utf-8") as f:
            json.dump(trigger, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        for key, value in trigger.items():
            if key in message.content:
                try:
                    await message.channel.send(value)
                except discord.HTTPException:
                    await message.channel.send('bros tag is longer than my pp :skull:')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tag(bot))