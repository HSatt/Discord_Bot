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
from atproto_client.exceptions import BadRequestError
from cogs.utils.diyembed import diyembed

# チャンネル指定
Manage_Channel = 1273134816308625439

# ずんだもん
zunda = 'https://i.imgur.com/6bgRNLR.png'

# Blueskyから情報を持ってくる
bsky_client = Client("https://api.bsky.app") # botに入れるならbsky_clientとかのほうがわかりやすいかも - おけ！

bsky_followed = {}
with open("data/bsky_followed.json", "r", encoding="utf-8") as f:
    bsky_followed = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
print('Successfully loaded previous bsky_followed record!')

# MAKE IT COGGY
class bluesky(commands.Cog): # ファイル名と同じにすると良い
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    # latestコマンドの定義
    @commands.command(
        name="latest", # コマンドの名前
        aliases=["ima"] 
    )
    async def latest(self, ctx):
        "名取さなさんの今をお届け！"
        await self.natori(ctx, 1)

    # blueskyコマンドの定義
    # 画像チェッㇰ
    image_red = False
    # 中身
    def bluesky(self, id, num: int):
        """Blueskyユーザーの最新投稿を取得"""
        num -= 1
        target_uri = bsky_client.get_author_feed(id).feed[num].post.uri
        useless = target_uri.split('/')
        try:
            self.bsky_image = bsky_client.get_author_feed(id).feed[num].post.embed.images[0].fullsize
            self.image_red = False
        except AttributeError:
            if self.image_red == True:
                pass
            else:
                print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] No Image Detected, Replaced with Placeholder.')
                self.bsky_image = ''
                self.image_red = True
            return
        finally:
            self.bsky_embed = diyembed.getembed(title = f"Latest Post from {id}", color=0x1084fd, 
                                                    description=bsky_client.get_author_feed(id).feed[num].post.record.text, 
                                                    title_url=f'https://bsky.app/profile/{id}/post/{useless[-1]}', 
                                                    author_name='BlueskyストーカーBot', author_url="https://satt.carrd.co/",
                                                    author_icon=bsky_client.get_author_feed(id).feed[num].post.author.avatar,
                                                    thumbnail="https://image.example.com/thumbnail.png",
                                                    image=self.bsky_image,
                                                    field1_name="Like ❤", field1_value=bsky_client.get_author_feed(id).feed[num].post.like_count,
                                                    field2_name="Repost ♻️", field2_value=bsky_client.get_author_feed(id).feed[num].post.repost_count,
                                                    footer_text="Pasted by Satt", footer_icon=zunda
                                                    )
            return self.bsky_embed


    # natoriコマンドの定義
    @commands.command(
        name="natori", # コマンドの名前。設定しない場合は関数名
    )
    async def natori(self, ctx, num: int):
        """名取さなさんの投稿を取得"""
        await ctx.send(embed=await self.bluesky("natorisana.com", num)) # embedの送信には、embed={定義したembed名}

    # bfollowコマンドの定義
    async def bfollow(self, ctx, id):
        """blueskyのユーザーをフォローするコマンド: fbridge.pyのfollowからしかトリガーされません"""
        try:
            bsky_followed[id] = bsky_client.get_author_feed(id).feed[0].post.record.text
            with open("data/bsky_followed.json", "w+", encoding="utf-8") as f: # フォロー一覧をセーブする
                json.dump(bsky_followed, f)
            with open(f"data/Server/bsky_followed/{ctx.guild.id}.json", "r", encoding="utf-8") as f: # サーバーごとのフォロー一覧を読み込む
                guild_bsky_followed = json.load(f)
            if not id in guild_bsky_followed:
                guild_bsky_followed.append(id)
                with open(f"data/Server/bsky_followed/{ctx.guild.id}.json", "w+", encoding="utf-8") as f: # サーバーごとのフォロー一覧をセーブする
                    json.dump(guild_bsky_followed, f)
                await ctx.reply(f'Succesfully followed {id} in Bluesky!\nRecent post:{bsky_followed[id]}')
                print(f'Succesfully followed {id} in Bluesky!\nRecent post:{bsky_followed[id]}')
            else:
                await ctx.reply(f'Already following {id}!')
                print(f'Already following {id}!')
        except BadRequestError as e: # BlueskyのIDが間違っている場合出るらしい 一か月前の自分に聞いてくれ
            await ctx.reply(f'The id you typed is invalid!!!!!!!!!!!: {e}')
            return

    # initializeコマンドの定義
    @commands.command()
    async def initialize(self, ctx):
        """InfStalkを動かすコマンド; 管理者権限が必要"""
        if ctx.author.guild_permissions.administrator:
            await ctx.send('initialized infstalk')
            await self.InfStalk()
        else:
            await ctx.send("nope")

    # InfStalk
    async def InfStalk(self):
        """Blueskyを10秒おきに覗く"""
        self.dupe_red = False
        channel = self.bot.get_channel(Manage_Channel)
        while True:
            for id, prev_post in bsky_followed.items():
                if prev_post == bsky_client.get_author_feed(id).feed[0].post.record.text:
                    if self.dupe_red == True: # ログがたくさん出るので、一回だけ出すようにする
                        continue
                    else:
                        print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] Same Post Detected, None will be sent.')
                        self.dupe_red = True
                else:
                    print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] \033[1m !!New Post Detected!! \033[0m')
                    bsky_embed = await self.bluesky(id, 1)
                    with open("data/Server/channels.json", "r", encoding="utf-8") as f: # サーバーごとの通知チャンネルを読み込む
                        channels = json.load(f)
                    for key, channel_id in channels.items():
                        with open(f"data/Server/bsky_followed/{key}.json", "r", encoding="utf-8") as f: # サーバーごとのフォロー一覧を読み込む
                            guild_followed = json.load(f)
                        for followed_id in guild_followed:
                            if followed_id == id:
                                channel = self.bot.get_channel(channel_id)
                                await channel.send(embed=bsky_embed)
                            else:
                                pass
                    bsky_followed[id] = bsky_client.get_author_feed(id).feed[0].post.record.text 
                    with open("data/bsky_followed.json", "w+", encoding="utf-8") as f:
                        json.dump(bsky_followed, f)
                    self.dupe_red = False
            await asyncio.sleep(5)  # これを使うといい感じに眠れるらしい...🫠
    
    @commands.Cog.listener()
    async def on_ready(self) -> None: # selfめっちゃ大事！！！！！！！！ 
        # BlueSkyを10秒おきに読み込む
        await self.InfStalk()

async def setup(bot: commands.Bot):

    await bot.add_cog(bluesky(bot))

