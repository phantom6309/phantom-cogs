import discord
from redbot.core import commands
from redbot.core import Config
from instaloader import Post
import re

class Insta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_global(login=True, password=True
        )



    @commands.command()
    async def giriş(self, ctx, login:str, password:str):
     await self.config.login.set(login)
     await self.config.password.set(password)
     await ctx.send("hesap ayarlandı!")
    
    @commands.command()
    async def insta(self, ctx, url:str):
        url = re.search(r'/p (.+?)/', url)
        login  = await self.config.login()
        password = await self.config.password()
        L = instaloader.Instaloader()
        L.login(login, password)
        post = Post.from_shortcode(L.context, url)
        await ctx.send(post)
        
      
