# this is utils not cogs frfr no cap
import discord
from discord.ext import commands
import json
class nosj(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    def load(file):
        with open(file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        return loaded
    
    @staticmethod
    def save(target, file):
        with open(file, "r", encoding="utf-8") as f:
            json.dump(target, f)
        print("dumped")
       
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(nosj(bot))