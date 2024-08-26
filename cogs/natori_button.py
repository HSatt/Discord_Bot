import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
import random

path = "./data/sana"
dirs = [f for f in os.listdir(path) if os.path.isdir(path + "/" + f)]
voices = []

# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'

for dir in dirs:
    if dir == "venv":
        continue
    files = os.listdir(path + "/" + dir)
    for file in files:
        file_path = dir + "/" + file
        voices.append(file_path)

# MAKE IT COGGY
class natori_button(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def natoriplayloop(self, ctx: Context) -> None:
        voice_path = random.choice(voices)
        ctx.voice_client.play(
            discord.FFmpegPCMAudio(voice_path), after=lambda e: self.natoriplayloop(ctx)
        )

    @commands.command(
        name="natoriplay", # コマンドの名前。設定しない場合は関数名
        aliases=['playnatori', 'nplay', 'pnatori', 'nsound']
    )
    async def natoriplay(self, ctx, voice_path):
        if ctx.author.voice is None:
            await ctx.reply("vc はいらんかい")

        if ctx.voice_client is not None:
            if ctx.voice_client.is_playing():
                await ctx.reply("今話してっから待ちなさい！")
                return

        try:
            await ctx.author.voice.channel.connect()
        except Exception as e:
            print(e)
        ctx.voice_client.play(
            discord.FFmpegPCMAudio(path + "/" + voice_path), after=None
        )

    @commands.command()
    async def inf(self, ctx: Context) -> None:
        print("a")
        if ctx.author.voice is None:
            await ctx.reply("vc はいらんかい")

        if ctx.voice_client is not None:
            if ctx.voice_client.is_playing():
                await ctx.reply("今話してっから待ちなさい！")
                return

        try:
            await ctx.author.voice.channel.connect()
        except Exception as e:
            print(e)

        self.natoriplayloop(ctx)

    @commands.command()
    async def nsearch(self, ctx, query):
        l_in = [s for s in voices if query in s]
        result = ''
        prev_result = l_in[0].split('/')[0]
        result += f'{l_in[0].split('/')[0]}\n'
        for directory in l_in:
            if directory.split('/')[0] != prev_result:
                result += f'{directory.split('/')[0]}\n'
                prev_result = directory.split('/')[0]
            result += f'**└**{directory.split('/')[1]}\n'
        self.natori_embed = discord.Embed( # Embedを定義する
                              title = f"""You searched for "{query}"...""",# タイトル
                              color = 0x1084fd, # フレーム色指定
                              description = result, # Embedの説明文
                              url = f'https://github.com/sanabutton/sounds' # これを設定すると、タイトルが指定URLへのリンクになる
                              )
        self.natori_embed.set_author(name = '名取さなの音声再生bot', # Botのユーザー名
                        url = "https://satt.carrd.co/", # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
                        icon_url = zunda # Botのアイコンを設定してみる
                        )
        self.natori_embed.set_thumbnail(url='https://yt3.googleusercontent.com/Qj-lyidMW6xtEdnv6rDYscGE1kO6K06-i4v8Eiij96YOTo_WdBboLVlEKeE3749ywpyqTec2=s160-c-k-c0x00ffffff-no-rj')
        self.natori_embed.set_footer(text = "Pasted by Satt", # フッターには開発者の情報でも入れてみる
                            icon_url = zunda)
        try:
            await ctx.reply(embed=self.natori_embed)
        except discord.HTTPException:
            await ctx.reply("うわーん！リストが長すぎます！")
            print(l_in)


    @commands.command()
    async def ping(self, ctx: Context) -> None:
        await ctx.reply("pong")

async def setup(bot: commands.Bot):
    await bot.add_cog(natori_button(bot))