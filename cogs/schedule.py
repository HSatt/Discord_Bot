from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import discord
from discord.ext import commands

async def send_message(channel, message):
    await channel.send(message)

def schedule_message(send_time, channel, message):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, 'date', run_date=send_time, args=[channel, message])
    scheduler.start()

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def schedule(self, ctx, time_str, message, channel_id=None):

        date = datetime.now()

        run_time = datetime.strptime(time_str, '%m/%d-%H:%M').replace(year=date.year)

        # Check if it's in the future
        now = datetime.now()
        delay = (run_time - now).total_seconds()
        assert delay > 0

        # Get the channel
        if channel_id is not None:
            channel = self.bot.get_channel(int(channel_id))
        else:
            channel = ctx.channel
        assert channel is not None

        # Schedule the message
        schedule_message(run_time, channel, message)

        # Confirm
        print(f"Scheduled a message at {run_time} in channel {channel}: {message}")
        await ctx.channel.send(f"All set, message wil be sent in {delay / 60:.2f} minutes (unless this bot crashes in meantime)!")

async def setup(bot):
    await bot.add_cog(Schedule(bot))