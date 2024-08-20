import discord
from discord.ext import commands
from discord.ext.commands import Context


class E(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["E"])
    async def e(self, ctx: Context) -> None:
        await ctx.reply("e", mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(E(bot))
