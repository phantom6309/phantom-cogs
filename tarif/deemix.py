# -*- coding: utf-8 -*-
import discord
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import bundled_data_path
from redbot.core.data_manager import cog_data_path
from deezfacu import Login
from deezfacu.__easy_spoty__ import Spo

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
    async def downspo(self, ctx, url, quality):
       arl = await self.config.token()
       downloa = Login(arl) 
       downloa.download_trackdee(
        url,
	output_dir = str(bundled_data_path(self)),
     	quality_download = quality,
	recursive_quality = False,
	recursive_download = False,
        not_interface = True,
        method_save = 2,
        )
       files = os.listdir(output_dir)
       for file_name in files:
        # create a file object for the current file
        file = discord.File(os.path.join(folder_path, file_name), filename=file_name)

        # send the file to the channel
        await channel.send(file=file)
        await ctx.send("tamamlandı")
    
