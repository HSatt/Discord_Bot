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
from typing import NoReturn
from twikit import Client, Tweet
from twikit.errors import ServerError
# チャンネル指定
Manage_Channel = 1273134816308625439

###########################################
CHECK_INTERVAL = 60 * 10 # チェック間隔
USER_ID = '0' # Placeholder
client = Client( # これが無いとTwitterにアクセスできない
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
                )
# MAKE IT COGGY
class tweet(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # ログイン情報を cookies.json から読み込む
        client.load_cookies("data/!important/cookies.json")
        # アカウント指定
        global followed
        followed = {}
        with open("data/tweet.json", "r", encoding="utf-8") as f:
            # tweet.jsonを開く(r)
            followed = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
            print('Successfully loaded previous followed record!')
            print(followed)
        global before_tweet
        before_tweet = {}
        # ユーザーネームからユーザーidをget
        global screen_name
        global handshake
        print(f'loading previous tweets...')
        # 過去のtweetをgetする
        with open("data/before_tweet.json", "r", encoding="utf-8") as f:
            # before_tweet.jsonを開く(r)
            before_tweet = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
        print(f'\033[1m>>>>> {before_tweet} <<<<<\033[0m')
        # 無限ストーカー編
        while True:
            for screen_name, handshake in followed.items():
                try:
                    print(f'loading {screen_name}({handshake})’s tweets...')
                    global latest_tweet
                    latest_tweet = {}
                    temp_latest_tweet = await self.get_latest_tweet(handshake)
                    latest_tweet[screen_name] = temp_latest_tweet.created_at_datetime.timestamp()
                    for tweets in await client.get_user_tweets(handshake, 'Tweets'):
                        if before_tweet[screen_name] < tweets.created_at_datetime.timestamp():
                            await self.callback(tweets)
                        else:
                            break
                    before_tweet[screen_name] = latest_tweet[screen_name]
                    await self.save_before_tweet()
                except ServerError:
                    channel = self.bot.get_channel(Manage_Channel)
                    await channel.send(f'''Failed to fetch {screen_name}'s tweets: We're being ratelimited or the api is down.''')
                    print(f'''Failed to fetch {screen_name}'s tweets: We're being ratelimited or the api is down.''')
            await asyncio.sleep(CHECK_INTERVAL)

    async def callback(self, tweet: Tweet) -> None:
        print(f'\033[1m>>>>> New tweet posted from @{screen_name}({handshake}) <<<<<\033[0m')
        channel = self.bot.get_channel(Manage_Channel)
        await channel.send(f'New tweet posted from {screen_name}({handshake}): https://fxtwitter.com/{handshake}/status/{tweet.id}')

    async def get_latest_tweet(self, user_id: int) -> Tweet:
        tweets = await client.get_user_tweets(user_id, 'Tweets')
        print(tweets)
        return tweets[0]
    
    @commands.command(
        name="fetch_tweet", # コマンドの名前。設定しない場合は関数名
        aliases=['tweet'],
        desctiption='人のつい～とを取ってきてくれるコマンドです'
    )
    async def fetch_tweet(self, ctx, screen_name: str, order: int) -> Tweet:
        try:
            user = await client.get_user_by_screen_name(screen_name)
            temp_user_id = user.id
            tweets = await client.get_user_tweets(temp_user_id, 'Tweets')
            print(tweets)
            tweets_list = tweets[order - 1]
            await ctx.reply(f'A tweet posted from {screen_name}({temp_user_id}): https://fxtwitter.com/{screen_name}/status/{tweets_list.id}')
        except:
            await ctx.reply('The user you typed is either suspended or misspelled.')
    
    async def save_before_tweet(self):
        with open("data/before_tweet.json", "w+", encoding="utf-8") as f:
            json.dump(before_tweet, f)
        print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] Succesfully saved {screen_name}’s tweets!')

    @commands.command(
        name="follow", # コマンドの名前。設定しない場合は関数名
    )
    async def follow(self, ctx, name: str):
        try:
            user = await client.get_user_by_screen_name(name)
            temp_user_id = user.id
            followed[name] = temp_user_id
            print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] Succesfully followed {name}!')
            await ctx.reply(f'Succesfully followed [{name}](https://x.com/{name})!')
            with open("data/tweet.json", "w+", encoding="utf-8") as f:
                json.dump(followed, f)
            print(f'loading {name}({temp_user_id}) tweets...')
            # 過去のtweetをgetする
            temp_before_tweet = await self.get_latest_tweet(temp_user_id)
            before_tweet[name] = temp_before_tweet.created_at_datetime.timestamp()
            print(f'\033[1m>>>>> {before_tweet} <<<<<\033[0m')
        except:
            await ctx.reply('The user you typed is either suspended or misspelled.')
    
    @commands.command(
        name="unfollow", # コマンドの名前。設定しない場合は関数名
    )
    async def unfollow(self, ctx, name: str):
        try:
            del followed[name]
            print(f'[{datetime.datetime.now().strftime('%H:%M:%S')}] Succesfully unfollowed {name}!')
            await ctx.reply(f'Succesfully unfollowed [{name}](https://x.com/{name})!')
            with open("data/tweet.json", "w+", encoding="utf-8") as f:
                json.dump(followed, f)
        except:
            await ctx.reply('The user you typed is not followed.')
        
async def setup(bot: commands.Bot):
    await bot.add_cog(tweet(bot))