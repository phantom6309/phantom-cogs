# -*- coding: utf-8 -*-
import discord
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import cog_data_path
from deezloader import Login

class Deemix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_global(token=True)
        
        
    
    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def setbaz(self, ctx, token):
     await self.config.token.set(token)
     await ctx.send("profil ayarlandı!")
        
    @commands.command()
    async def download(self, ctx, url,quality):
       arl = await self.config.token()
       downloa = Login(arl) 
       fp = downloa.download_trackdee(url,
	output_dir = str(cog_data_path(self) ),
	quality_download = quality,
	recursive_quality = False,
	recursive_download = False,
        not_interface = False,
        method_save = 1
        )
       file = discord.File(str(fp), filename=şarkı)
            try:
                await ctx.send(files=[file])
            except Exception:
                log.error("Error sending crabrave video", exc_info=True)
                pass
            try:
                os.remove(fp)
            except Exception:
                log.error("Error deleting crabrave video", exc_info=True)
