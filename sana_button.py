import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="button ", intents=intents)
path = "./data/sounds/sana"
dirs = [f for f in os.listdir(path) if os.path.isdir(path + "/" + f)]
voices = []


for dir in dirs:
    if dir == "venv":
        continue
    files = os.listdir(path + "/" + dir)
    for file in files:
        file_path = dir + "/" + file
        voices.append(file_path)

def playloop(ctx: Context) -> None:
    voice_path = random.choice(voices)
    ctx.voice_client.play(
        discord.FFmpegPCMAudio(voice_path), after=lambda e: playloop(ctx)
    )

@bot.command()
async def play(ctx, voice_path):
    if ctx.author.voice is None:
        await ctx.reply("vc はいらんかい")

    if ctx.voice_client is not None:
        if ctx.voice_client.is_playing():
            await ctx.reply("今話してっから待ちなさい！")
            return

    try:
        await ctx.author.voice.channel.connect()
    except Exception as e:
        print(e)
    ctx.voice_client.play(
        discord.FFmpegPCMAudio(path + "/" + voice_path), after=None
    )

@bot.command()
async def inf(ctx: Context) -> None:
    print("a")
    if ctx.author.voice is None:
        await ctx.reply("vc はいらんかい")

    if ctx.voice_client is not None:
        if ctx.voice_client.is_playing():
            await ctx.reply("今話してっから待ちなさい！")
            return

    try:
        await ctx.author.voice.channel.connect()
    except Exception as e:
        print(e)

    playloop(ctx)

@bot.command()
async def search(ctx, query):
    l_in = [s for s in voices if query in s]
    print(l_in)
    await ctx.reply(l_in)

@bot.command()
async def ping(ctx: Context) -> None:
    await ctx.reply("pong")


bot.run("OTI1MzYwMDgyMDA5NjEyMzMw.G6l99e.7Qe9fH_9dPH8w9nLZ9ch030HC02NNZtrE1DBBk")