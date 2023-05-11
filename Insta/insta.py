import discord
from redbot.core import commands
from redbot.core import Config
import instaloader

class Insta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_member( login=None, 
            password=None)



    @commands.command()
    async def giriş(self, ctx):
        await ctx.author.send("kullanıcı adınızı giriniz")
        login = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("şifrenizi giriniz?")
        password = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)


        await self.config.member(ctx.author).login.set(login.content)
        await self.config.member(ctx.author).password.set(password.content)

        
        await ctx.send("Profiliniz başarıyla oluşturuldu!")
    
    @commands.command()
    async def insta(self, ctx, url:str):
        url = re.search(r'/p (.+?)/', url).group(1)
        L = instaloader.Instaloader()
        L.login(login, password)
        post = Post.from_shortcode(L.context, url)
        await ctx.send(post)
        
      
