# -*- coding: utf-8 -*-
import discord
import os
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import bundled_data_path
from redbot.core.data_manager import cog_data_path
from deezfacu import Login
import glob

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
           for filename in files:
               decoded_filename = filename.encode('iso-8859-1').decode('utf-8')
               decoded_filename = decoded_filename.replace(" ", "_")
               with open(os.path.join(root, filename), 'rb') as f:
                    file_data = discord.File(f, filename=decoded_filename)
                    await ctx.send(file=file_data)
           os.remove(os.path.join(root, filename))
       await ctx.send("tamamlandı")
