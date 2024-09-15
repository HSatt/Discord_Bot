import discord
from discord.ext import commands
import random
from atproto import Client # type: ignore
import asyncio
import json
from cogs.diyembed import diyembed
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

# MAKE IT COGGY
class random(commands.Cog): # xyzはcogの名前(ファイル名と同じにすると良いぞ)(違っても良い)(好きにしな)
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
    async def announce(self, ctx, comment):
        if ctx.author.id == 754839099260665877:
            with open("data/Server/channels.json", "r", encoding="utf-8") as f:
                channels = json.load(f)
            for Key, Announce_Channel in channels.items():
                channel = self.bot.get_channel(Announce_Channel)
                announce = await channel.send(comment)
                await ctx.send(f"Sent {comment}: https://discord.com/channels/{Key}/{Announce_Channel}/{announce.id}")

    @commands.command()
    async def add_channel(self, ctx, channel_id):
        with open("data/Server/channels.json", "r", encoding="utf-8") as f:
            channels = json.load(f)
        channel = self.bot.get_channel(int(channel_id))
        try:
            await channel.send("This channel is now listening to events!")
            await ctx.reply("Added the channel!")
            channels[str(ctx.guild.id)] = int(channel_id)
            with open("data/Server/channels.json", "w+", encoding="utf-8") as f:
                json.dump(channels, f)
            with open(f"data/Server/bsky_followed/{ctx.guild.id}.json", "w+", encoding="utf-8") as f:
                json.dump({}, f)
        except discord.HTTPException:
            await ctx.reply("The channel ID you sent is invalid!")
            return
        
    @commands.command()
    async def sex(self, ctx, message_id):
        await ctx.message.delete()
        message = await ctx.fetch_message(int(message_id))
        await message.add_reaction("🇸")
        await message.add_reaction("🇪")
        await message.add_reaction("🇽")

async def setup(bot: commands.Bot): 
    await bot.add_cog(random(bot))