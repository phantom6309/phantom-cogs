# -*- coding: utf-8 -*-
import discord
import os
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import bundled_data_path
from redbot.core.data_manager import cog_data_path
from deezfacu import Login
import ftfy

class Deemix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_global(token=True
        )
        
        
    
    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def setarl(self, ctx, token):
     await self.config.token.set(token)
     await ctx.send("arl ayarlandı!")
        
    
    @commands.command()
    async def downspo(self, ctx, url, quality = None):
       if quality == None:
          quality = "FLAC"
       arl = await self.config.token()
       downloa = Login(arl) 
       downloa.download_trackspo(
        url,
	output_dir = str(bundled_data_path(self)),
     	quality_download = quality,
	recursive_quality = False,
	recursive_download = False,
        not_interface = True,
        method_save = 1,
        )    
       path = str(bundled_data_path(self))
       for root, dirs, files in os.walk(path):
          for file_name in files:
           try:
                with open(os.path.join(root, file_name), "rb") as file:
                    filename = file_name.encode('utf-8').decode('utf-8')
                    file_data = discord.File(file, filename=filename)
                    await ctx.send(file=file_data)
           except UnicodeDecodeError:
                pass
           finally:
                os.remove(os.path.join(root, file_name))

       await ctx.send("tamamlandı")
