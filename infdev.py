import discord
from discord.ext import commands
from atproto import Client # type: ignore
import json
import pretty_help
from pretty_help import PrettyHelp
import datetime
initial_extensions = (
    "cogs.getnatori", 
    "cogs.fuck",
    "cogs.delete",
    "cogs.gamble",
    "cogs.youtube",
    "cogs.tweet",
    "cogs.e",
    "cogs.diyembed",
    "cogs.hypixel",
    "cogs.voice"
)

description = '''Hello.
There are a number of utility commands being showcased here.
co-developped by donotsolveme
(I illegally steal codes from various people)
(including donotsolveme)'''

# チャンネル指定
Manage_Channel = 1273134816308625439

# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'

# help
# embedの下の文字
ending_note = "Pasted by Satt \nFor help: {help.clean_prefix}{help.invoked_with}"

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='*',
                         description=description,
                         intents=intents,
                         help_command=PrettyHelp(menu=pretty_help.AppMenu(),
                                                 index_title="Do you need any help?",
                                                 color= 0x191919,
                                                 ending_note=ending_note,
                                                 thumbnail_url=zunda,
                                                 send_typing=False,
                                                 sort_commands=True
                                                 )
                        ) # ここにcommands.Botで使ってたパラメータを入れる
    
    async def setup_hook(self) -> None: # ログインする前に実行されるイベント
        await bot.load_extension("jishaku")
        for extension in initial_extensions: 
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(e)
                print(f"Failed to load extension {extension}.")

    async def on_ready(self):
        print(f'Logged in as {self.user.name}#{self.user.discriminator} ({self.user.id})')
        channel = bot.get_channel(Manage_Channel)
        await channel.send(f'The Bot is up! @ {datetime.datetime.now().strftime("%H:%M:%S")}')

bot = MyBot()
bot_token = ''
with open("data/!important/bot_token.json", "r", encoding="utf-8") as f:
    bot_token = json.load(f)

bot.run(bot_token)
