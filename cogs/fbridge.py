import discord
from discord.ext import commands
from discord.ui import Button, View
import random
from atproto import Client # type: ignore
import asyncio
import json
from cogs.utils.diyembed import diyembed
from cogs.bluesky import bluesky
from cogs.twitter import twitter
from cogs.youtube import youtube
# buttons
class Follow_Bridge(View):
    def __init__(self, ctx, target_id):
        super().__init__()
        self.ctx = ctx
        self.target_id = target_id

    @discord.ui.button(emoji="<:bsky:1284434214510395442>", label="Bluesky", style=discord.ButtonStyle.green)
    async def bsky_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Bluesky上の{self.target_id}をフォローします…", ephemeral=True)
        await bluesky.bfollow(self, self.ctx, self.target_id)
    
    @discord.ui.button(emoji="<:twitter:1284435019917430835>", label="Twitter", style=discord.ButtonStyle.green)
    async def twitter_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Twitter上の{self.target_id}をフォローします…", ephemeral=True)
        await twitter.tfollow(self, self.ctx, self.target_id)

    @discord.ui.button(emoji="<:youtube:1284353556836778024>", label="Youtube", style=discord.ButtonStyle.green)
    async def youtube_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Youtube上の{self.target_id}をフォローします…", ephemeral=True)
        self.target_id = await youtube.convert(self, self.ctx, self.target_id)
        await youtube.sub(self, self.ctx, self.target_id)
        
class follow(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def follow(self, ctx, target_id):
        view = Follow_Bridge(ctx, target_id)
        await ctx.reply(view=view, embed=await diyembed.getembed(title=f"""どのプラットフォームで"{target_id}"をフォローしますか？""", color=0x1084fd,))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(follow(bot))