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
from cogs.diyembed import diyembed
# チャンネル指定
Manage_Channel = 1273134816308625439
# target list
fucked = []
items = [
    "歯", "靴", "金属（例えば、銀）", "宝石", "車のボディ", "鏡", "メガネ", "木材", 
    "陶器", "ステンレス", "ガラス", "メタルフィギュア", "時計", "銅製品", "銀器", 
    "磁器", "照明器具", "スチール", "アルミニウム", "レザー製品", "チタン", "金", 
    "ステンレス製のカトラリー", "アクセサリー", "タイル", "プラスチック", "銅線", 
    "シルバーアクセサリー", "ノートパソコンの表面", "スマートフォン", "カメラレンズ", 
    "音楽機器", "彫刻", "家具", "イヤリング", "ブレスレット", "リング", "ペンダント", 
    "スポーツ用具", "自転車のフレーム", "ヘルメット", "メダル", "ビンの口", 
    "磨き仕上げされた石", "アート作品", "眼鏡のフレーム", "すり鉢", "すりこぎ", 
    "鋼材", "磨かれた大理石", "自動車部品", "ドアノブ", "銀のカップ", "風鈴", 
    "酒器", "スポーツカップ", "ペンケース", "織物の装飾", "磨き上げられたトロフィー", 
    "工具", "アンティーク家具", "鉄製品", "電子機器の筐体", "金属製の装飾品", "ホイール", 
    "キッチン用品", "スポーツウェア（光沢加工されたもの）", "襟章", "高級筆記具", 
    "研磨剤で磨かれた木彫り", "革製のベルト", "ステンレス製の調理器具", "スポーツボトル", 
    "美術品のフレーム", "メタルパーツ（機械の一部）", "陶磁器", "木製の楽器", 
    "高級タバコケース", "ビリヤードのキュー", "船の部品", "武道の装備", 
    "楽器の金属部分", "医療機器", "スポーツ用具（クラブなど）", "カメラのボディ", 
    "音響機器", "装飾的な金属パーツ", "磨き上げられた真鍮製品", "釣り具", 
    "高級ワインのボトル", "名刺入れ", "電気器具", "金属製の家具部品", "高級な鍵", 
    "アートのフレーム", "スポーツのメダル", "車のホイールリム", "歴史的な硬貨", 
    "装飾的な宝飾品", "高級時計のケース"
]
trigger = {}
with open("data/trigger.json", "r", encoding="utf-8") as f:
# bank_info.jsonを開く(r)
    trigger = json.load(f) # dataにファイル(f)をjsonとしてロードしたものを入れる
print('Successfully loaded previous trigger record!')

# MAKE IT COGGY
class fuck(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # fuckコマンドの定義
    @commands.command(
        name="fuck", # コマンドの名前。設定しない場合は関数名
        aliases=["hi", "hey"] # ?hiでも ?heyでも反応するようになる
    )
    async def fuck(self, ctx):
        await ctx.reply(f'Fuck Off {ctx.author.mention}')

    @commands.command()
    async def migaku(self, ctx):
        migaku_item = random.choice(items)
        await ctx.reply(f'今日は**{migaku_item}**を磨きましょう')
        
    @commands.command(
        name="mass_mention", # コマンドの名前。設定しない場合は関数名
        aliases=["mass", "mass_murder"], # ?hiでも ?heyでも反応するようになる
        description="targetを10回mentionするだけです"
    )
    async def mass_mention(self, ctx, target):
        for i in range(10):
            msg = await ctx.send(f'Fuck Off <@{target}>')
            fucked.append(msg.id)
        print(fucked)

    @commands.command(
        name="sorry", # コマンドの名前。設定しない場合は関数名
        aliases=[";;", "forgiveme", "gomen", "soy", "so-ri-", "sry"], # ?hiでも ?heyでも反応するようになる
        description="targetを10回mentionするだけです"
    )
    async def sorry(self, ctx):
        while fucked != []:
            for delete in fucked:
                try:
                    # メッセージIDを使ってメッセージオブジェクトを取得
                    message = await ctx.channel.fetch_message(delete)
                    await message.delete()
                    await ctx.send(f'Message with ID {delete} has been deleted.', delete_after=5)
                    fucked.remove(delete)
                except discord.NotFound:
                    await print('Message not found.')
                    return
                except discord.Forbidden:
                    await print('I do not have permission to delete this message.')
                    return
                except discord.HTTPException:
                    await print('Failed to delete message.')
                    return
                finally:
                    await asyncio.sleep(0.1)
        print(fucked)

    @commands.command()
    async def tag(self, ctx, mode, key, *, value=''):
        if mode == 'create':
            trigger[key] = value
            print(f'Succesfully created: {key} for {trigger[key]}!')
            try:
                await ctx.reply(f'Succesfully created: {key} for {trigger[key]}!')
            except discord.HTTPException:
                await ctx.reply('bros tag is longer than my pp :skull:')
        elif mode == 'remove':
            try:
                removed = trigger.pop(key)
                print(f'Succesfully removed: {key} for {removed}!')
                await ctx.reply(f'Succesfully removed: {key} for {removed}!')
            except KeyError:
                await ctx.reply('The key you entered does not exist in the list.')
                return
        else:
            await ctx.reply('You need to use either create or remove to use this command!')
        with open("data/trigger.json", "w+", encoding="utf-8") as f:
            json.dump(trigger, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        for key, value in trigger.items():
            if key in message.content:
                try:
                    await message.channel.send(value)
                except discord.HTTPException:
                    await message.channel.send('bros tag is longer than my pp :skull:')


async def setup(bot: commands.Bot):
    await bot.add_cog(fuck(bot))