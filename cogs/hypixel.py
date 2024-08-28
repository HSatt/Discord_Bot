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

# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'

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

     # uuid command
    @commands.command(
            name="sheepwars",
            aliases=["shw", "sheep"]
            )
    async def sheepwars(self, ctx, query):
        # mojang API
        mojang_data = getInfo(f'https://api.mojang.com/users/profiles/minecraft/{query}')
        uuid = mojang_data["id"]

        # hypixel API
        hypixel_url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
        hypixel_data = getInfo(hypixel_url)
        with open(f"data/hypixel/{query}.json", "w+", encoding="utf-8") as f:
            json.dump(hypixel_data, f)
        stat = hypixel_data["player"]["stats"]["WoolGames"]["sheep_wars"]["stats"]
        embed = self.bot.get_command("embed")
        await ctx.reply(embed=await embed(ctx, title=f"{query}'s stats in Sheep Wars",
                                          description=f"**Total games played:** {stat["games_played"]}\n**└Wins:** {stat["wins"]}\n**└Losses:** {stat["losses"]}\n **-** W/L Ratio: {round(stat["wins"] / stat["losses"], 3)}",
                                          author_name='Hypixel API grabber', author_url='https://satt.carrd.co/',author_icon=zunda, thumbnail='', image='',
                                          field1_name='💀 Kills:', field1_value=stat["kills"],
                                          field2_name='🪦 Deaths:', field2_value=stat["deaths"], footer_text="Pasted by Satt", footer_icon=zunda))

async def setup(bot: commands.Bot):
    await bot.add_cog(hypixel(bot))