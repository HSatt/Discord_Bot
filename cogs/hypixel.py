import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import requests
import datetime
from cogs.diyembed import diyembed
import base64
import urllib.request
def getInfo(call):
    r = requests.get(call)
    return r.json()
# hypixel API
api_key = ''
with open("data/!important/temp_hypixel_api.json", "r", encoding="utf-8") as f:
    api_key = json.load(f)

# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'

global zom_page
zom_page = 0

# buttons
class MyView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
    async def left_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MyView()
        global zom_page
        zom_page += 1
        if zom_page > 4:
            zom_page = 0
        await interaction.response.edit_message(embed=await diyembed.getembed(self, title=f"{title} / Page {zom_page + 1}",
                                            description=f"{zom_response[zom_page]}",
                                            author_name='Hypixel API grabber', author_url='https://satt.carrd.co/',author_icon=zunda, thumbnail="attachment://temp.png", image='',
                                            footer_text="Pasted by Satt", footer_icon=zunda), view=view)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
    async def right_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MyView()
        global zom_page
        zom_page += 1
        if zom_page > 4:
            zom_page = 0
        await interaction.response.edit_message(embed=await diyembed.getembed(self, title=f"{title} / Page {zom_page + 1}",
                                            description=f"{zom_response[zom_page]}",
                                            author_name='Hypixel API grabber', author_url='https://satt.carrd.co/',author_icon=zunda, thumbnail="attachment://temp.png", image='',
                                            footer_text="Pasted by Satt", footer_icon=zunda), view=view)

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
    
    @commands.command()
    async def skin(self, ctx, query):
        # Mojang APIからプレイヤーのプロフィールを取得
        mojang_data = getInfo(f'https://api.mojang.com/users/profiles/minecraft/{query}')
        uuid = mojang_data["id"]
        profile_url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        response = requests.get(profile_url)
        
        if response.status_code != 200:
            raise Exception("Failed to get profile information")
        
        profile_data = response.json()
        
        # プロフィール情報からスキンのURLを取得
        properties = profile_data.get("properties", [])
        for prop in properties:
            if prop["name"] == "textures":
                texture_data = base64.b64decode(prop["value"]).decode("utf-8")
                texture_json = json.loads(texture_data)
                skin_url = texture_json["textures"]["SKIN"]["url"]
                await ctx.reply(skin_url)
                return skin_url
        raise Exception("Skin URL not found")
    
    async def get_head_url(self, query):
        # mojang API
        mojang_data = getInfo(f'https://api.mojang.com/users/profiles/minecraft/{query}')
        uuid = mojang_data["id"]
        # ヘッドの画像URLを生成
        urllib.request.urlretrieve(f"https://crafatar.com/avatars/{uuid}", "data/head.png")

        

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

    # sheepwars command
    @commands.command(
            name="sheepwars",
            aliases=["shw", "sheep"]
            )
    async def sheepwars(self, ctx, query):
        hypixel_data = await self.get_uuid_data(ctx, query)
        skin_url = await self.get_head_url(query)
        try:
            stats = hypixel_data["player"]["stats"]["WoolGames"]["sheep_wars"]["stats"]
        except KeyError:
            await ctx.reply('fuck you idiot')
        
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
        file = discord.File("data/head.png", filename="temp.png")
        await ctx.reply(file=file, embed=await diyembed.getembed(self, title=f"{query}'s stats in Sheep Wars 🐑⚔️",
                                          description=f"{desc}\n\n **-** **Default Kit:** {hypixel_data["player"]["stats"]["WoolGames"]["sheep_wars"]["default_kit"].title()}",
                                          author_name='Hypixel API grabber', author_url='https://satt.carrd.co/',author_icon=zunda, thumbnail="attachment://temp.png", image='',
                                          footer_text="Pasted by Satt", footer_icon=zunda))
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Done fetching {query}'s data!")

    # zombies command
    @commands.command(
            name="zombies",
            aliases=["zom", "zombie"]
            )
    async def zombies(self, ctx, query):
        global zom_response
        zom_response = []
        zom_page = 0
        hypixel_data = await self.get_uuid_data(ctx, query)
        skin_url = await self.get_head_url(query)
        try:
            global stats_arcade
            stats_arcade = hypixel_data["player"]["stats"]["Arcade"]
        except KeyError:
            await ctx.reply('fuck you idiot')
        view = MyView()
        

        zom_stats_main = {"""\- D/W Ratio: """: "dwratio",
                          "\n┗Wins: ": "wins_zombies", "\nᅠ┣Wins in DeadEnd: ": "wins_zombies_deadend", "\nᅠ┣Wins in BadBlood: ": "wins_zombies_badblood",
                          "\nᅠ┣Wins in Alien Arcadium: ": "wins_zombies_alienarcadium", "\nᅠ┗Wins in Prison: ": "wins_zombies_prison",
                          "\n┗Deaths: ": "deaths_zombies", "\nᅠ┣Deaths in DeadEnd: ": "deaths_zombies_deadend", "\nᅠ┣Deaths in BadBlood: ": "deaths_zombies_badblood",
                          "\nᅠ┣Deaths in Alien Arcadium: ": "deaths_zombies_alienarcadium", "\nᅠ┗Deaths in Prison: ": "deaths_zombies_prison",
                          """\n\- K/D Ratio: """: "kdratio", "\n┗Kills: ": "zombie_kills_zombies",}
        desc = ''
        for key, value in zom_stats_main.items():
            desc += await self.zom_get_data(key, value)
        zom_response.append(desc)

        zom_stats_wins = {"""\- D/W Ratio: """: "dwratio",
                     "\n┗Wins: ": "wins_zombies",
                     "\nᅠ┗Wins in DeadEnd: ": "wins_zombies_deadend", "\nᅠᅠ┣Wins in DE Normal: ": "wins_zombies_deadend_normal",
                     "\nᅠᅠ┣Wins in DE Hard: ": "wins_zombies_deadend_hard", "\nᅠᅠ┗Wins in DE RIP: ": "wins_zombies_deadend_rip",
                     "\nᅠ┗Wins in BadBlood: ": "wins_zombies_badblood", "\nᅠᅠ┣Wins in BB Normal: ": "wins_zombies_badblood_normal",
                     "\nᅠᅠ┣Wins in BB Hard: ": "wins_zombies_badblood_hard", "\nᅠᅠ┗Wins in BB RIP: ": "wins_zombies_badblood_rip",
                     "\nᅠ┗Wins in Alien Arcadium: ": "wins_zombies_alienarcadium",
                     "\nᅠ┗Wins in Prison: ": "wins_zombies_prison", "\nᅠᅠ┣Wins in Normal: ": "wins_zombies_prison_normal", 
                     "\nᅠᅠ┣Wins in Hard: ": "wins_zombies_prison_hard", "\nᅠᅠ┗Wins in RIP: ": "wins_zombies_prison_rip",
                     "\n┗Deaths: ": "deaths_zombies",
                     }
        desc = ''
        for key, value in zom_stats_wins.items():
            desc += await self.zom_get_data(key, value)
        zom_response.append(desc)
        
        zom_stats_deaths = {"""\- D/W Ratio: """: "dwratio", 
                            "\n┗Wins: ": "wins_zombies",
                            "\n┗Deaths: ": "deaths_zombies",
                            "\nᅠ┗Deaths in DeadEnd: ": "deaths_zombies_deadend", "\nᅠᅠ┣Deaths in DE Normal: ": "deaths_zombies_deadend_normal",
                            "\nᅠᅠ┣Deaths in DE Hard: ": "deaths_zombies_deadend_hard", "\nᅠᅠ┗Deaths in DE RIP: ": "deaths_zombies_deadend_rip",
                            "\nᅠ┗Deaths in BadBlood: ": "deaths_zombies_badblood", "\nᅠᅠ┣Deaths in BB Normal: ": "deaths_zombies_badblood_normal",
                            "\nᅠᅠ┣Deaths in BB Hard: ": "deaths_zombies_badblood_hard", "\nᅠᅠ┗Deaths in BB RIP: ": "deaths_zombies_badblood_rip",
                            "\nᅠ┗Deaths in Alien Arcadium: ": "deaths_zombies_alienarcadium",
                            "\nᅠ┗Deaths in Prison: ": "deaths_zombies_prison", "\nᅠᅠ┣Deaths in Normal: ": "deaths_zombies_prison_normal", 
                            "\nᅠᅠ┣Deaths in Hard: ": "deaths_zombies_prison_hard", "\nᅠᅠ┗Deaths in RIP: ": "deaths_zombies_prison_rip",
                            }
        desc = ''
        for key, value in zom_stats_deaths.items():
            desc += await self.zom_get_data(key, value)
        zom_response.append(desc)

        zom_stats_kills = {"""\- K/D Ratio: """: "kdratio",
                           "\n┗Deaths: ": "deaths_zombies",
                          "\n┗Kills: ": "zombie_kills_zombies",
                          "\nᅠ┗Kills in DeadEnd: ": "zombie_kills_zombies_deadend", "\nᅠᅠ┣Kills in DE Normal: ": "zombie_kills_zombies_deadend_normal",
                          "\nᅠᅠ┣Kills in DE Hard: ": "zombie_kills_zombies_deadend_hard", "\nᅠᅠ┗Kills in DE RIP: ": "zombie_kills_zombies_deadend_rip",
                          "\nᅠ┗Kills in BadBlood: ": "zombie_kills_zombies_badblood", "\nᅠᅠ┣Kills in BB Normal: ": "zombie_kills_zombies_badblood_normal",
                          "\nᅠᅠ┣Kills in BB Hard: ": "zombie_kills_zombies_badblood_hard", "\nᅠᅠ┗Kills in BB RIP: ": "zombie_kills_zombies_badblood_rip",
                          "\nᅠ┗Kills in Alien Arcadium: ": "zombie_kills_zombies_alienarcadium",
                          "\nᅠ┗Kills in Prison: ": "zombie_kills_zombies_prison", "\nᅠᅠ┣Kills in Normal: ": "zombie_kills_zombies_prison_normal", 
                          "\nᅠᅠ┣Kills in Hard: ": "zombie_kills_zombies_prison_hard", "\nᅠᅠ┗Kills in RIP: ": "zombie_kills_zombies_prison_rip",
                         }
        desc = ''
        for key, value in zom_stats_kills.items():
            desc += await self.zom_get_data(key, value)
        zom_response.append(desc)
        
        zom_stats_all = {"""\- D/W Ratio: """: "dwratio",
                     "\n┗Wins: ": "wins_zombies",
                     "\nᅠ┗Wins in DeadEnd: ": "wins_zombies_deadend", "\nᅠᅠ┣Wins in DE Normal: ": "wins_zombies_deadend_normal",
                     "\nᅠᅠ┣Wins in DE Hard: ": "wins_zombies_deadend_hard", "\nᅠᅠ┗Wins in DE RIP: ": "wins_zombies_deadend_rip",
                     "\nᅠ┗Wins in BadBlood: ": "wins_zombies_badblood", "\nᅠᅠ┣Wins in BB Normal: ": "wins_zombies_badblood_normal",
                     "\nᅠᅠ┣Wins in BB Hard: ": "wins_zombies_badblood_hard", "\nᅠᅠ┗Wins in BB RIP: ": "wins_zombies_badblood_rip",
                     "\nᅠ┗Wins in Alien Arcadium: ": "wins_zombies_alienarcadium",
                     "\nᅠ┗Wins in Prison: ": "wins_zombies_prison", "\nᅠᅠ┣Wins in Normal: ": "wins_zombies_prison_normal", 
                     "\nᅠᅠ┣Wins in Hard: ": "wins_zombies_prison_hard", "\nᅠᅠ┗Wins in RIP: ": "wins_zombies_prison_rip",
                     "\n┗Deaths: ": "deaths_zombies",
                     "\nᅠ┗Deaths in DeadEnd: ": "deaths_zombies_deadend", "\nᅠᅠ┣Deaths in DE Normal: ": "deaths_zombies_deadend_normal",
                     "\nᅠᅠ┣Deaths in DE Hard: ": "deaths_zombies_deadend_hard", "\nᅠᅠ┗Deaths in DE RIP: ": "deaths_zombies_deadend_rip",
                     "\nᅠ┗Deaths in BadBlood: ": "deaths_zombies_badblood", "\nᅠᅠ┣Deaths in BB Normal: ": "deaths_zombies_badblood_normal",
                     "\nᅠᅠ┣Deaths in BB Hard: ": "deaths_zombies_badblood_hard", "\nᅠᅠ┗Deaths in BB RIP: ": "deaths_zombies_badblood_rip",
                     "\nᅠ┗Deaths in Alien Arcadium: ": "deaths_zombies_alienarcadium",
                     "\nᅠ┗Deaths in Prison: ": "deaths_zombies_prison", "\nᅠᅠ┣Deaths in Normal: ": "deaths_zombies_prison_normal", 
                     "\nᅠᅠ┣Deaths in Hard: ": "deaths_zombies_prison_hard", "\nᅠᅠ┗Deaths in RIP: ": "deaths_zombies_prison_rip",
                     """\n\- K/D Ratio: """: "kdratio",
                     "\n┗Kills: ": "zombie_kills_zombies",
                     "\nᅠ┗Kills in DeadEnd: ": "zombie_kills_zombies_deadend", "\nᅠᅠ┣Kills in DE Normal: ": "zombie_kills_zombies_deadend_normal",
                     "\nᅠᅠ┣Kills in DE Hard: ": "zombie_kills_zombies_deadend_hard", "\nᅠᅠ┗Kills in DE RIP: ": "zombie_kills_zombies_deadend_rip",
                     "\nᅠ┗Kills in BadBlood: ": "zombie_kills_zombies_badblood", "\nᅠᅠ┣Kills in BB Normal: ": "zombie_kills_zombies_badblood_normal",
                     "\nᅠᅠ┣Kills in BB Hard: ": "zombie_kills_zombies_badblood_hard", "\nᅠᅠ┗Kills in BB RIP: ": "zombie_kills_zombies_badblood_rip",
                     "\nᅠ┗Kills in Alien Arcadium: ": "zombie_kills_zombies_alienarcadium",
                     "\nᅠ┗Kills in Prison: ": "zombie_kills_zombies_prison", "\nᅠᅠ┣Kills in Normal: ": "zombie_kills_zombies_prison_normal", 
                     "\nᅠᅠ┣Kills in Hard: ": "zombie_kills_zombies_prison_hard", "\nᅠᅠ┗Kills in RIP: ": "zombie_kills_zombies_prison_rip",
                     }
        desc = ''
        for key, value in zom_stats_all.items():
            desc += await self.zom_get_data(key, value)
        zom_response.append(desc)
        global title
        title = f"{query}'s stats in Zombies 🧟‍♀️⚔️"
        global message
        file = discord.File("data/head.png", filename="temp.png")
        message = await ctx.reply(file=file, embed=await diyembed.getembed(self, title=f"{title} / Page 1",
                                          description=f"{zom_response[zom_page]}",
                                          author_name='Hypixel API grabber', author_url='https://satt.carrd.co/',author_icon=zunda, thumbnail="attachment://temp.png", image='',
                                          footer_text="Pasted by Satt", footer_icon=zunda), view=view)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Done fetching {query}'s data!")

    async def zom_get_data(self, key, value):
        data = ''
        data += f"**{key}**"
        try:
            if value == "dwratio":
                data += str(round(stats_arcade["deaths_zombies"] / stats_arcade["wins_zombies"], 3))
            elif value == "kdratio":
                data += str(round(stats_arcade["zombie_kills_zombies"] / stats_arcade["deaths_zombies"], 3))
            else:
                data += f"{stats_arcade[value]:,}"
        except KeyError:
            data += ">> 0 <<"
        return data

    async def left(self):
        view = MyView()
        global zom_page
        zom_page -= 1
        if zom_page < 0:
            zom_page = 4
        await hypixel.editing(self, view=view)

    async def right(self):
        view = MyView()
        global zom_page
        zom_page += 1
        if zom_page > 4:
            zom_page = 0
        await hypixel.editing(self, view=view)

    async def editing(self, view):
        await message.edit(embed=await diyembed.getembed(self, title=f"{title} / Page {zom_page + 1}",
                                            description=f"{zom_response[zom_page]}",
                                            author_name='Hypixel API grabber', author_url='https://satt.carrd.co/',author_icon=zunda, thumbnail='', image='',
                                            footer_text="Pasted by Satt", footer_icon=zunda), view=view)
async def setup(bot: commands.Bot):
    await bot.add_cog(hypixel(bot))