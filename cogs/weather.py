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
                weathers.append(weather.get_text())
            for item in tag:
                desc += item
                if item in ("┣最高気温", "┗最低気温"):
                    desc += ": " + contents.pop(0)
                elif item in ("- 今日の気象情報", "- 明日の気象情報"):
                    desc += ": " + weathers.pop(0)
                desc += "\n"
            await ctx.reply(embed=await diyembed.getembed(self, title=f"""{pref}/{region}の天気""", description=f"""{desc}""", color=0x1084fd,))
        else:
            await ctx.reply("go tenki jp idiot")
            print("go tenki jp idiot")
            raise Exception("go tenki jp idiot")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(weather(bot))