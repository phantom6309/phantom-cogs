# -*- coding: utf-8 -*-
import discord
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import cog_data_path
import deezloader


class Deemix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_guild(email=None, 
         password=None
         )
        
        
    
    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def setbaz(self, ctx, mail,passw):
     await self.config.guild(ctx.guild).email.set(mail)
     await self.config.guild(ctx.guild).password.set(passw)
     await ctx.send("profil ayarlandı!")
        
    @commands.command()
    async def download(self, ctx, url,quality):
       email = await self.config.guild(ctx.guild).email()
       password = await self.config.guild(ctx.guild).password() 
       downloa = Login(
	    email = my_deezer_email,
	    password = my_deezer_password
        )
       downloa.download_trackspo(
	    #YOUR SPOTIFY TRACK LINK,
	    output_dir =str(cog_data_path(self) / url),
	    quality_download = quality,
	    recursive_quality = True,
	    recursive_download = True,
	    not_interface = True,
	    method_save = 2
        )
