import discord
from discord.ext import commands
from discord.ext.commands import Context

zunda = 'https://i.imgur.com/6bgRNLR.png'
class diyembed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    async def getembed(title='', color=0x191919, description='', title_url='', author_name='', author_url='',
                    author_icon='', thumbnail='', image='', field1_name='', field1_value='', field2_name='', field2_value='',
                    footer_text='', footer_icon=''):
        embed = discord.Embed( # Embedを定義する
                              title = title, # タイトル
                              color = color, # フレーム色指定
                              description = description, # Embedの説明文
                              url = title_url # これを設定すると、タイトルが指定URLへのリンクになる
                              )
        embed.set_author(name = author_name, # Botのユーザー名
                         url = author_url, # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
                         icon_url = author_icon # Botのアイコンを設定してみる
                         )
        if thumbnail != None:
            embed.set_thumbnail(url = thumbnail) # サムネイルとして小さい画像を設定できる
        if image != None:
            embed.set_image(url = image) # 大きな画像タイルを設定できる
            embed.add_field(name = field1_name, value = field1_value) # フィールドを追加。
            embed.add_field(name = field2_name, value = field2_value)
            embed.set_footer(text = footer_text, # フッターには開発者の情報でも入れてみる
                                icon_url = footer_icon)
        return embed
async def setup(bot: commands.Bot):
    await bot.add_cog(diyembed(bot))
