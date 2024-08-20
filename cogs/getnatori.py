import discord
from discord.ext import commands
import random
import datetime
from atproto import Client # type: ignore
import time
import asyncio
from pyngrok import ngrok
from ytnoti import AsyncYouTubeNotifier, Video
import json

# チャンネル指定
Manage_Channel = 1273134816308625439

# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'

# Blueskyから情報を持ってくる
bsky_client = Client("https://api.bsky.app") # botに入れるならbsky_clientとかのほうがわかりやすいかも - おけ！

# MAKE IT COGGY
class getnatori(commands.Cog): # ファイル名と同じにすると良い
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    # latestコマンドの定義
    @commands.command(
        name="latest", # コマンドの名前
        aliases=["ima"] 
    )
    async def latest(self, ctx):
        await self.natori(ctx, 1)

    # getnatoriコマンドの定義
    # 画像チェッㇰ
    image_red = False
    # 中身
    def getnatori(self, num: int):
        num -= 1
        target_uri = bsky_client.get_author_feed("natorisana.com").feed[num].post.uri
        useless = target_uri.split('/')
        global image_red
        global bsky_embed
        global bsky_image
        try:
            self.bsky_image = bsky_client.get_author_feed("natorisana.com").feed[num].post.embed.images[0].fullsize
            self.image_red = False
        except AttributeError:
            if self.image_red == True:
                pass
            else:
                print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] No Image Detected, Replaced with Placeholder.')
                self.bsky_image = zunda
                self.image_red = True
            return
        finally:
            self.bsky_embed = discord.Embed( # Embedを定義する
                              title = "Latest Post From Sana Natori",# タイトル
                              color = 0x1084fd, # フレーム色指定
                              description = bsky_client.get_author_feed("natorisana.com").feed[num].post.record.text, # Embedの説明文
                              url = f'https://bsky.app/profile/natorisana.com/post/{useless[-1]}' # これを設定すると、タイトルが指定URLへのリンクになる
                              )
            self.bsky_embed.set_author(name = '名取さなのBlueskyストーカーBot', # Botのユーザー名
                         url = "https://satt.carrd.co/", # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
                         icon_url = bsky_client.get_author_feed("natorisana.com").feed[num].post.author.avatar # Botのアイコンを設定してみる
                         )
            self.bsky_embed.set_thumbnail(url = "https://image.example.com/thumbnail.png") # サムネイルとして小さい画像を設定できる
            self.bsky_embed.set_image(url = self.bsky_image) # 大きな画像タイルを設定できる
            self.bsky_embed.add_field(name = "Like ❤", value = bsky_client.get_author_feed("natorisana.com").feed[num].post.like_count) # フィールドを追加。
            self.bsky_embed.add_field(name = "Repost ♻️", value = bsky_client.get_author_feed("natorisana.com").feed[num].post.repost_count)
            self.bsky_embed.set_footer(text = "Pasted by Satt", # フッターには開発者の情報でも入れてみる
                                icon_url = zunda)
            return bsky_client.get_author_feed("natorisana.com").feed[1].post.record.text


    # natoriコマンドの定義
    @commands.command(
        name="natori", # コマンドの名前。設定しない場合は関数名
    )
    async def natori(self, ctx, num: int):
        self.getnatori(num)
        await ctx.send(embed = self.bsky_embed) # embedの送信には、embed={定義したembed名}

    # InfStalk
    async def InfStalk(self):
        self.prev_post = 'None'
        with open("data/prev_post.json", "r", encoding="utf-8") as f:
            self.prev_post = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
        self.dupe_red = False
        global bsky_embed
        channel = self.bot.get_channel(Manage_Channel)
        while True:
            self.getnatori(1)
            if self.prev_post == bsky_client.get_author_feed("natorisana.com").feed[1].post.record.text:
                if self.dupe_red == True:
                    pass
                else:
                    print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] Same Post Detected, None will be sent.')
                    self.dupe_red = True
            else:
                print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] \033[1m !!New Post Detected!! \033[0m')
                await channel.send(embed=self.bsky_embed)
                self.prev_post = bsky_client.get_author_feed("natorisana.com").feed[1].post.record.text  # コルーチンを実行する
                self.dupe_red = False
            await asyncio.sleep(5)  # これを使うといい感じに眠れるらしい...🫠
    
    @commands.Cog.listener()
    async def on_ready(self) -> None: # selfめっちゃ大事！！！！！！！！ 
        print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] We have logged in as {self.bot.user}')
        channel = self.bot.get_channel(Manage_Channel)
        await channel.send(f'The Bot is up! @ {datetime.datetime.now().strftime('%H:%M:%S')}')
        with open("data/prev_post.json", "w+", encoding="utf-8") as f:
            json.dump(self.getnatori(1), f)
        # 名取のBlueSkyを10秒おきに読み込む
        await self.InfStalk()

async def setup(bot: commands.Bot):
    await bot.add_cog(getnatori(bot))

