import discord
from redbot.core import commands
from redbot.core import Config
from redbot.core.data_manager import bundled_data_path
import instaloader
import os, shutil
import re
from twdown import TwdownAPI

class Insta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_global(login=True, password=True, twlogin=True, twpassword=True
        )
        


    @commands.command()
    async def giriş(self, ctx, login:str, password:str):
     await self.config.login.set(login)
     await self.config.password.set(password)
     await ctx.send("hesap ayarlandı!")
 
    @commands.command()
    async def giriştw(self, ctx, twlogin:str, twpassword:str):
     await self.config.twlogin.set(twlogin)
     await self.config.twpassword.set(twpassword)
     await ctx.send("hesap ayarlandı!")
    
    @commands.command()
    async def insta(self, ctx, url):
        login  = await self.config.login()
        password = await self.config.password()
        L = instaloader.Instaloader()
        L.login(login, password)
        download_loc = str(bundled_data_path(self)) 
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        L.download_video_thumbnails = False
        L.dirname_pattern = download_loc
        file=L.download_post(post, download_loc)
        path = str(bundled_data_path(self))
        for root, dirs, files in os.walk(path):
         for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".mp4", "jpg", "jpeg"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                  file = discord.File(str(filepath), filename)
                  await ctx.send(files=[file])
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)
                
    @commands.command()
    async def tw(self, ctx, url:str):
        twlogin  = await self.config.twlogin()
        twpassword = await self.config.twpassword()
         
        twdown = TwdownAPI(
        sharelink = url,
        dir_to_save =str(bundled_data_path(self))
        )  
        twdown.run()
        path = str(bundled_data_path(self))
        for root, dirs, files in os.walk(path):
         for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".mp4", "jpg", "jpeg"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                  file = discord.File(str(filepath), filename)
                  await ctx.send(files=[file])
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)
        
        
      
