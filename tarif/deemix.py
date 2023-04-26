# -*- coding: utf-8 -*-
import discord
import os
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import bundled_data_path
from redbot.core.data_manager import cog_data_path
from deezfacu import Login
import glob
from transfersh_client.app import send_to_transfersh

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
    async def parça(self, ctx, url, quality = None):
       if quality == None:
          quality = "MP3_320"
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
       for filepath in glob.iglob(path + '/**/*', recursive=True):
          if os.path.isfile(filepath):
           filename = os.path.basename(filepath)
           with open(filepath, "rb") as f:
               download_link = send_to_transfersh(filepath, clipboard=False)
               await ctx.send(download_link)
           os.remove(path)
       await ctx.send("tamamlandı")

    @commands.command()
    async def albüm(self, ctx, url, quality = None):
       if quality == None:
          quality = "MP3_320"
       arl = await self.config.token()
       downloa = Login(arl) 
       downloa.download_albumspo(
        url,
	output_dir = str(bundled_data_path(self)),
     	quality_download = quality,
	recursive_quality = False,
	recursive_download = False,
        not_interface = True,
        method_save = 1,
        make_zip = True
        )    
       path = str(bundled_data_path(self))
       zip_file=None
       for filepath in glob.iglob(path + '/**/*', recursive=True):
          if os.path.isfile(filepath):
           filename = os.path.basename(filepath)
           if filename.endswith(".zip"):
              zip_file = filepath
           elif zip_file is not None:
                os.remove(path)
       if zip_file is None:
        await ctx.send("Could not find ZIP file")
        return
       download_link = send_to_transfersh(zip_file, clipboard=False)
       os.remove(path)
       await ctx.send(download_link)
       await ctx.send("tamamlandı")
