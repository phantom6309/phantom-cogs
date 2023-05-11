import discord
from redbot.core import commands
from redbot.core import Config
import instaloader
from instaloader import Instaloader, Post
import re

class Insta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_global(login=True, password=True
        )
        
    def extract_shortcode(url):
     regex = r"(?<=instagram\.com/)(p|reel|tv|reels)/([\w-]+)"
     matches = re.search(regex, url)
     if matches:
        return matches.group(2)
     return None


    @commands.command()
    async def giriş(self, ctx, login:str, password:str):
     await self.config.login.set(login)
     await self.config.password.set(password)
     await ctx.send("hesap ayarlandı!")
    
    @commands.command()
    async def insta(self, ctx, url:str):
        shortcode = extract_shortcode(url)
        login  = await self.config.login()
        password = await self.config.password()
        L = instaloader.Instaloader()
        L.login(login, password)
        post = Post.from_shortcode(L.context, shortcode)
        video = L.download_post(post)
        await ctx.send(video)
        
      
