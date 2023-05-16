import discord
from redbot.core import commands
from redbot.core import Config
from redbot.core.data_manager import bundled_data_path
import os, shutil
import re
from twdown import TwdownAPI

class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
             
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
     twitter_link_pattern = r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/[\w\/]+"
     if re.search(twitter_link_pattern, message.content):
        urls = re.findall(twitter_link_pattern, message.content)
        for url in urls:
            twdown = TwdownAPI(
                sharelink=url,
                dir_to_save=str(bundled_data_path(self))
            )
            twdown.run()
            path = str(bundled_data_path(self))
            for root, dirs, files in os.walk(path):
                for filename in files:
                    ext = os.path.splitext(filename)[1]
                    if ext.lower() in [".mp4", ".jpg", ".jpeg"]:
                        filepath = os.path.join(root, filename)
                        with open(filepath, "rb") as f:
                            file = discord.File(filepath, filename)
                            await message.channel.send(files=[file])
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir() and not entry.is_symlink():
                        shutil.rmtree(entry.path)
                    else:
                        os.remove(entry.path)
                        
   
