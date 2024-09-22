from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import discord
from discord.ext import commands
from cogs.utils.nosj import nosj
from cogs.utils.diyembed import diyembed
from datetime import timedelta
import json

async def send_message(channel, message):
    await channel.send(message)

def schedule_message(send_time, channel, message):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, 'date', run_date=send_time, args=[channel, message])
    scheduler.start()

class schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def schedule(self, ctx, time_str, message, channel_id=None):
        """I literally stole this code from https://gist.github.com/arnodeceuninck/c3b06e30d66045fba56789f43d04260e"""
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

    async def doku_notification(self):
        channel = self.bot.get_channel(1273134816308625439)
        print(f"notified @ {datetime.now()}")
        await channel.send(embed=await diyembed.getembed(title="どくラジの時間だ！",
                                                         title_url="https://radiko.jp/#!/live/QRR",
                                                         description="そこのお前！\n名取さなの毒にも薬にもならないラジオはあと5分で始まるぜ！",
                                                         color=0x1084fd))
        doku_time = nosj.load("data/schedule/doku.json")
        doku_time = datetime.strptime(doku_time, '%Y/%m/%d-%H:%M') + timedelta(days=7)
        print(f"Next doku time: {doku_time}")
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.doku_notification, 'date', run_date=doku_time)
        scheduler.start()
        doku_time = doku_time.strftime('%Y/%m/%d-%H:%M')
        nosj.save(doku_time, "data/schedule/doku.json")

    @commands.Cog.listener()
    async def on_ready(self):
        doku_time = nosj.load("data/schedule/doku.json")
        doku_time = datetime.strptime(doku_time, '%Y/%m/%d-%H:%M')
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.doku_notification, 'date', run_date=doku_time)
        print(f"Scheduled doku notification at {doku_time}")
        scheduler.start()

async def setup(bot):
    await bot.add_cog(schedule(bot))