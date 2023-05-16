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
        self.config.register_global(login=True, password=True)
        
        


    @commands.command()
    async def giriş(self, ctx, login:str, password:str):
     await self.config.login.set(login)
     await self.config.password.set(password)
     await ctx.send("hesap ayarlandı!")
 
    

                
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
     instagram_link_pattern = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|tv|reel)\/[\w\/]+"
     if re.search(instagram_link_pattern, content):
        urls = re.findall(instagram_link_pattern, message.content)
        for url in urls:
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
