import discord
from discord.ext import commands
import json
import requests
import datetime
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

    # convert username to uuid, and get data from hypixel API
    async def get_uuid_data(self, ctx, query):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Grabbing {query}'s data from Hypixel API...")
        # mojang API
        mojang_data = getInfo(f'https://api.mojang.com/users/profiles/minecraft/{query}')
        uuid = mojang_data["id"]

        # hypixel API
        hypixel_url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
        hypixel_data = getInfo(hypixel_url)
        with open(f"data/hypixel/{query}.json", "w+", encoding="utf-8") as f:
            json.dump(hypixel_data, f)
        return hypixel_data
    
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
        hypixel_data = await self.get_uuid_data(ctx, query)
        try:
            stats = hypixel_data["player"]["stats"]["WoolGames"]["sheep_wars"]["stats"]
        except KeyError:
            await ctx.reply('fuck you idiot')
        embed = self.bot.get_command("embed")
        shw_stats = {"**Total Games played: **": "games_played",
                     "\n\n**-** **W/L Ratio: **": "wlratio", "\n**┗Wins: **": "wins", "\n**┗Losses: **": "losses",
                     "\n\n**-** **K/D Ratio: **": "kdratio", "\n**┗Total Kills: **": "kills", "\n**ᅠ┣Void Kills: **": "kills_void",
                     "\n**ᅠ┣Explosion Kills: **": "kills_explosive", "\n**ᅠ┣Bow Kills: **": "kills_bow", "\n**ᅠ┗Melee Kills: **": "kills_melee",
                     "\n**┗Total Deaths: **": "deaths", "\n**ᅠ┣Void Deaths: **": "deaths_void",
                     "\n**ᅠ┣Explosion Deaths: **": "deaths_explosive", "\n**ᅠ┣Bow Deaths: **": "deaths_bow", "\n**ᅠ┗Melee Deaths: **": "deaths_melee",
                     "\n\n**-** **Damage Dealt: **": "damage_dealt", " ❤️\n**-** **Sheep Thrown: **": "sheep_thrown",}
        desc = ''
        for key, value in shw_stats.items():
            desc += key
            try:
                if value == "wlratio":
                    desc += str(round(stats["wins"] / stats["losses"], 3))
                elif value == "kdratio":
                    desc += str(round(stats["kills"] / stats["deaths"], 3))
                else:
                    desc += str(stats[value])
            except KeyError:
                desc += "0"
        await ctx.reply(embed=await embed(ctx, title=f"{query}'s stats in Sheep Wars 🐑⚔️",
                                          description=desc,
                                          author_name='Hypixel API grabber', author_url='https://satt.carrd.co/',author_icon=zunda, thumbnail='', image='',
                                          footer_text="Pasted by Satt", footer_icon=zunda))
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Done fetching {query}'s data!")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(hypixel(bot))