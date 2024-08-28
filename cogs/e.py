import discord
from discord.ext import commands
from discord.ext.commands import Context


class E(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["E"])
    async def e(self, ctx: Context) -> None:
        await ctx.reply("e")
    
    @commands.command(aliases=["mogus"])
    async def amogus(self, ctx: Context) -> None:
        embed = self.bot.get_command("embed")
        await ctx.reply(embed=await embed(ctx, title='Play Among us now!', description='''"Among Us" is a multiplayer online game where players work together on a spaceship to complete tasks, 
                    but some are impostors trying to sabotage and eliminate the crew. Players must identify and vote out the impostors while impostors deceive and eliminate 
                    crew members without being caught. It's known for its social deduction gameplay.''', 
                    title_url='https://among.us', author_name='Among Us Promotion', author_url='https://among.us',
                    author_icon='https://i.imgur.com/YfUMLWc.png', thumbnail='https://i.imgur.com/YfUMLWc.png'
                    ))


async def setup(bot: commands.Bot):
    await bot.add_cog(E(bot))
