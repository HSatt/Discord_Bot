# テスト用です。
# 本当に終わっている機能しかないので、使わないほうがいいです。
# コメントもしません。

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View
from cogs.utils.diyembed import diyembed
import random

class MyView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
    async def left_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await E.left(self)
        await interaction.response.send_message("Left Button clicked!", ephemeral=True)
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
    async def right_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await E.right(self)
        await interaction.response.send_message("Right Button clicked!", ephemeral=True)

class E(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(aliases=["E"])
    async def e(self, ctx: Context) -> None:
        await ctx.reply("e")
    
    @commands.command(aliases=["mogus"])
    async def amogus(self, ctx: Context) -> None:
        view = MyView()
        global message
        
        message = await ctx.reply(embed=await diyembed.getembed(title='Play Among us now!', description='''"Among Us" is a multiplayer online game where players work together on a spaceship to complete tasks, 
                    but some are impostors trying to sabotage and eliminate the crew. Players must identify and vote out the impostors while impostors deceive and eliminate 
                    crew members without being caught. It's known for its social deduction gameplay.''', 
                    title_url='https://among.us', author_name='Among Us Promotion', author_url='https://among.us',
                    author_icon='https://i.imgur.com/YfUMLWc.png', thumbnail='https://i.imgur.com/YfUMLWc.png'
                    ), view=view)

    async def left(self):
        view = MyView()
        await message.edit(content="left", embed=None, view=view)

    async def right(self):
        view = MyView()
        await message.edit(content="right", embed=None, view=view)

    @commands.command(aliases=["rap, cap"])
    async def nap(self, ctx: Context) -> None:
        await ctx.reply(f"今日は**{random.randrange(1, 100)}**分昼寝しましょう！")

async def setup(bot: commands.Bot):
    await bot.add_cog(E(bot))
