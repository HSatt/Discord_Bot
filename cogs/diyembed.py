import discord
from discord.ext import commands
from discord.ext.commands import Context

zunda = 'https://i.imgur.com/6bgRNLR.png'
class diyembed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(
        name="embed", # コマンドの名前。設定しない場合は関数名
    )
    async def embed(self, ctx, title=None, description=None, title_url=None, author_name=None, author_url=None,
                    author_icon=zunda, thumbnail=zunda, image=zunda, field1_name='', field1_value='', field2_name='', field2_value='',
                    footer_text="Pasted by Satt", footer_icon=zunda):
        self.embed = discord.Embed( # Embedを定義する
                              title = title,# タイトル
                              color = 0x191919, # フレーム色指定
                              description = description, # Embedの説明文
                              url = title_url # これを設定すると、タイトルが指定URLへのリンクになる
                              )
        self.embed.set_author(name = author_name, # Botのユーザー名
                         url = author_url, # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
                         icon_url = author_icon # Botのアイコンを設定してみる
                         )
        if thumbnail != None:
            self.embed.set_thumbnail(url = thumbnail) # サムネイルとして小さい画像を設定できる
        if image != None:
            self.embed.set_image(url = image) # 大きな画像タイルを設定できる
        if field1_name or field1_value != None:
            self.embed.add_field(name = field1_name, value = field1_value) # フィールドを追加。
        if field2_name or field2_value != None:
            self.embed.add_field(name = field2_name, value = field2_value)
        if footer_text or footer_icon != None:
            self.embed.set_footer(text = footer_text, # フッターには開発者の情報でも入れてみる
                                icon_url = footer_icon)
        await ctx.send(embed=self.embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(diyembed(bot))
