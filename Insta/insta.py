import discord
from redbot.core import commands
from redbot.core import Config
from redbot.core.data_manager import bundled_data_path
import instaloader
import os, shutil
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
    async def insta(self, ctx, url):
        login  = await self.config.login()
        password = await self.config.password()
        L = instaloader.Instaloader()
        L.login(login, password)
        download_loc = str(bundled_data_path(self))
        try:
            post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
            L.download_video_thumbnails = False
            L.dirname_pattern = download_loc
            file=L.download_post(post, download_loc)
            await ctx.send(file)
            with os.scandir(download_loc) as entries:
             for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)
        except instaloader.exceptions.ProfileNotExistsException:
            await ctx.send ("Invalid URL or the video is not available")
        
      
