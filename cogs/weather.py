import discord
from discord.ext import commands
from discord.ui import Button, View
import random
from atproto import Client # type: ignore
import asyncio
import json
import requests
from bs4 import BeautifulSoup
from cogs.diyembed import diyembed

weather_irons = {'晴': '<:weather_01:1285278839018098800>', 
                 '晴一時曇': '<:weather_02:1285278840809324555>', 
                 '晴一時雨': '<:weather_03:1285278842440650833>', 
                 '晴一時雪': '<:weather_04:1285278844072362056>', 
                 '晴のち曇': '<:weather_05:1285278845825450025>', 
                 '晴のち雨': '<:weather_06:1285278847239192690>', 
                 '晴の ち雪': '<:weather_07:1285278848681906287>', 
                 '曇': '<:weather_08:1285278850175074304>', 
                 '曇一時晴': '<:weather_09:1285278851525644351>', 
                 '曇一時雨': '<:weather_10:1285278853081595979>', 
                 '曇一時雪': '<:weather_11:1285278854780420167>', 
                 '曇のち晴': '<:weather_12:1285278856806268998>', 
                 '曇のち雨': '<:weather_13:1285278858014101627>', 
                 '曇のち雪': '<:weather_14:1285278859604000809>', 
                 '雨': '<:weather_15:1285278860681806020>', 
                 '雨一時晴': '<:weather_16:1285278862531493940>', 
                 '雨時々曇': '<:weather_17:1285278863739326506>', 
                 '雨一時雪': '<:weather_18:1285278865522032650>', 
                 '雨のち晴': '<:weather_19:1285278866503368787>', 
                 '雨のち曇': '<:weather_20:1285278868718096516>', 
                 '雨のち雪': '<:weather_21:1285278870542749808>', 
                 '暴風雨': '<:weather_22:1285278871926738986>', 
                 '雪': '<:weather_23:1285278873013063736>', 
                 '雪一時晴': '<:weather_24:1285278874728534169>', 
                 '雪一時曇': '<:weather_25:1285278876464975993>', 
                 '雪一時雨': '<:weather_26:1285278877630861413>', 
                 '雪のち晴': '<:weather_27:1285278879178686667>', 
                 '雪のち曇': '<:weather_28:1285278880323731497>', 
                 '雪のち雨': '<:weather_29:1285278882018099221>', 
                 '暴風雪': '<:weather_30:1285278883389771910>', 
                 '晴一時雨か雪': '<:weather_31:1285278884756979792>', 
                 '晴一時雪か雨': '<:weather_32:1285278886426447882>', 
                 '晴のち雨か雪': '<:weather_33:1285278887940460644>', 
                 '晴のち雪か雨': '<:weather_34:1285278889391947841>', 
                 '曇一時雨か雪': '<:weather_35:1285278890977136792>', 
                 '曇一時雪か雨': '<:weather_36:1285278892428624007>', 
                 '曇のち雨か雪': '<:weather_37:1285278893879591043>', 
                 '曇のち雪か雨': '<:weather_38:1285278895452586136>', 
                 '雨か雪': '<:weather_39:1285278896815738890>', 
                 '雨か雪 のち晴': '<:weather_40:1285278898246123650>', 
                 '雨か雪のち曇': '<:weather_41:1285278899823050794>', 
                 '雪か雨': '<:weather_42:1285278902045900821>', 
                 '雪か雨のち晴': '<:weather_43:1285278903757443143>', 
                 '雪か雨のち曇': '<:weather_44:1285278905380503582>'}
# MAKE IT COGGY
class weather(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, pref, region):
        tenki_url = 'https://tenki.jp/'
        response = requests.get(tenki_url)

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(response.content, 'lxml')

        # クラス名 'forecast-entry-13116' を持つ要素を検索
        forecast_entry = soup.find("a", string=pref)
        if forecast_entry:
            pref_link = f"https://tenki.jp{forecast_entry.get("href")}"
            print(pref_link)
        else:
            print("go tenki jp idiot")
            await ctx.reply("go tenki jp idiot")
            raise Exception("go tenki jp idiot")


        url = pref_link
        response = requests.get(url)

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(response.content, 'lxml')

        # クラス名 'forecast-entry-13116' を持つ要素を検索
        forecast_entry = soup.find("a", string=region)
        if forecast_entry:
            region_link = f"https://tenki.jp{forecast_entry.get("href")}"
            print(region_link)
        else:
            await ctx.reply("go tenki jp idiot")
            print("go tenki jp idiot")
            raise Exception("go tenki jp idiot")

        url = region_link
        response = requests.get(url)

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(response.content, 'lxml')

        forecast_entry = soup.find_all("dd")
        print(forecast_entry)
        if forecast_entry:
            desc = ""
            count = 0
            temp_content = ""
            contents = []
            warnings = []
            alerts = []
            tag = ["- 今日の気象情報", "┣最高気温", "┗最低気温", "- 明日の気象情報", "┣最高気温", "┗最低気温"]
            for content in forecast_entry:
                if "warn-entry" in str(content):
                    warnings.append(content.get_text())
                elif "alert-entry" in str(content):
                    alerts.append(content.get_text())
                else:
                    temp_content += content.get_text()
                    if count == 1:
                        contents.append(temp_content)
                        temp_content = ""
                        count = 0
                    else:
                        count += 1
            print(contents[0])
            if warnings != []:
                desc += "**警報**:\n"
                for warning in warnings:
                    desc += f"{warning}\n"
            if alerts != []:
                desc += "**注意報**:\n"
                for alert in alerts:
                    desc += f"{alert}\n"
            weather_telop = soup.find_all(class_="weather-telop")
            print(weather_telop)
            weathers = []
            for weather in weather_telop:
                weathers.append(weather_irons[weather.get_text()] + " " + weather.get_text())
            for item in tag:
                desc += item
                if item in ("┣最高気温", "┗最低気温"):
                    desc += ": " + contents.pop(0)
                elif item in ("- 今日の気象情報", "- 明日の気象情報"):
                    desc += ": " + weathers.pop(0)
                desc += "\n"
            await ctx.reply(embed=await diyembed.getembed(self, title=f"""{pref}/{region}の天気""", description=f"""{desc}""", color=0x1084fd))
        else:
            await ctx.reply("go tenki jp idiot")
            print("go tenki jp idiot")
            raise Exception("go tenki jp idiot")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(weather(bot))