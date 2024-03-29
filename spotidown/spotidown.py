# -*- coding: utf-8 -*-
import discord
import os, shutil
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import bundled_data_path
from deezfacu import Login
import re
from fileio_wrapper import Fileio

class Spotidown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_global(token=True, api=True
        )
     
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        urls = re.findall(r"(https?://[^\s]+)", message.content)
        quality = None
        channel = message.channel
        if "MP3_320" in message.content:
            quality = "MP3_320"
        elif "FLAC" in message.content:
            quality = "FLAC"

        for url in urls:
            if "open.spotify.com/track/" in url:
                await self.spoparça(channel, url, quality)

        for url in urls:
            if "open.spotify.com/album/" in url:
                await self.spoalbum(channel, url, quality)
    
    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def setarl(self, ctx, token):
     await self.config.token.set(token)
     await ctx.send("arl ayarlandı!")
	
    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def setapi(self, ctx, api):
     await self.config.api.set(api)
     await ctx.send("api ayarlandı!")
        
    
    @commands.command()
    async def spoparça(self, ctx, url, quality = None):
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
       for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".mp3", ".flac", ".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                 file = discord.File(filepath, filename)
                 await ctx.send(files=[file])  
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)

    @commands.hybrid_command()
    async def parça(self, ctx, artist,song, quality = None):
       if quality == None:
          quality = "MP3_320"
       arl = await self.config.token()
       downloa = Login(arl) 
       downloa.download_name(
        artist,
        song,
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
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".mp3", ".flac", ".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                 file = discord.File(filepath, filename)

                 await ctx.send(files=[file])  
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)


    @commands.command()
    async def spoalbüm(self, ctx, url, quality = None):
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
        make_zip = False
        )    
       path = str(bundled_data_path(self))
       for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in ["mp3","flac",".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                 file = discord.File(filepath, filename)
                 await ctx.send(files=[file])   
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)


    @commands.command()
    async def spolist(self, ctx, url, quality = None):
       if quality == None:
          quality = "MP3_320"
       arl = await self.config.token()
       downloa = Login(arl) 
       path = str(bundled_data_path(self))
       downloa.download_playlistspo(
        url,
	output_dir =path,
     	quality_download = quality,
	recursive_quality = False,
	recursive_download = False,
        not_interface = True,
        method_save = 1,
        make_zip = False
        )    
       
       for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in ["mp3","flac",".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                 file = discord.File(filepath, filename)
                 await ctx.send(files=[file])   
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)

    @commands.command()

    async def deeparça(self, ctx, url, quality = None):

       if quality == None:

          quality = "MP3_320"

       arl = await self.config.token()

       downloa = Login(arl) 

       downloa.download_trackdee(

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

            ext = os.path.splitext(filename)[1]

            if ext.lower() in [".mp3", ".flac", ".zip"]:

                filepath = os.path.join(root, filename)

                with open(filepath, "rb") as f:

                 fileio_api_key = await self.config.api()

                 fileio = Fileio(fileio_api_key)

                 resp = Fileio.upload(filepath)

                 link = resp['link']

                 await ctx.send(link)   

       with os.scandir(path) as entries:

            for entry in entries:

                if entry.is_dir() and not entry.is_symlink():

                   shutil.rmtree(entry.path)

                else:

                   os.remove(entry.path)
                
