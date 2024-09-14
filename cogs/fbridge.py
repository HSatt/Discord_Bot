import discord
from discord.ext import commands
from discord.ui import Button, View
import random
from atproto import Client # type: ignore
import asyncio
import json
from cogs.diyembed import diyembed
from cogs.bluesky import bluesky
from cogs.tweet import tweet
from cogs.youtube import youtube
# buttons
class Follow_Bridge(View):
    def __init__(self, ctx, target_id):
        super().__init__()
        self.ctx = ctx
        self.target_id = target_id

    @discord.ui.button(emoji="<:youtube:1284353556836778024>", label="Bluesky", style=discord.ButtonStyle.primary)
    async def bsky_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Bluesky上の{self.target_id}をフォローします…", ephemeral=True)
        await bluesky.bfollow(self, self.ctx, self.target_id)
    
    @discord.ui.button(label="Twitter", style=discord.ButtonStyle.primary)
    async def twitter_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Twitter上の{self.target_id}をフォローします…", ephemeral=True)
        await tweet.follow(self, self.ctx, self.target_id)

    @discord.ui.button(label="Youtube", style=discord.ButtonStyle.primary)
    async def youtube_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Youtube上の{self.target_id}をフォローします…", ephemeral=True)
        self.target_id = await youtube.convert(self, self.ctx, self.target_id)
        await youtube.subscribe(self, self.ctx, self.target_id)
        
class follow(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def follows(self, ctx, target_id):
        view = Follow_Bridge(ctx, target_id)
        await ctx.reply(view=view, embed=await diyembed.getembed(self, title=f"""どのプラットフォームで"{target_id}"をフォローしますか？""", color=0x1084fd,))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(follow(bot))