import discord
from discord.ext import commands
import json
import requests

def getInfo(call):
    r = requests.get(call)
    return r.json()

# hypixel API
api_key = ''
with open("data/!important/temp_hypixel_api.json", "r", encoding="utf-8") as f:
    api_key = json.load(f)

# MAKE IT COGGY
class hypixel(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # uuid command
    @commands.command()
    async def uuid(self, ctx, query):
        # mojang API
        mojang_data = getInfo(f'https://api.mojang.com/users/profiles/minecraft/{query}')
        uuid = mojang_data["id"]

        # hypixel API
        hypixel_url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
        hypixel_data = getInfo(hypixel_url)
        with open(f"data/hypixel/{query}.json", "w+", encoding="utf-8") as f:
            json.dump(hypixel_data, f)
        stat = hypixel_data["player"]["uuid"]
        await ctx.reply(stat)

async def setup(bot: commands.Bot):
    await bot.add_cog(hypixel(bot))