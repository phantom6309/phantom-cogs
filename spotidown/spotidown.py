# -*- coding: utf-8 -*-
import discord
import os, shutil
from redbot.core import checks,commands,Config 
from redbot.core.data_manager import bundled_data_path
from deezfacu import Login
from transfersh_client.app import send_to_transfersh

class Spotidown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7364528762)
        self.config.register_global(token=True
        )
        
        
    
    @commands.hybrid_command()
    @checks.admin_or_permissions(manage_guild=True)
    async def setarl(self, ctx, token):
     await self.config.token.set(token)
     await ctx.send("arl ayarlandı!")
        
    
    @commands.hybrid_command()
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
                  download_link = send_to_transfersh(filepath, clipboard=False)
                  await ctx.send(download_link)
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)


    @commands.hybrid_command()
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
        make_zip = True
        )    
       path = str(bundled_data_path(self))
       for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                  download_link = send_to_transfersh(filepath, clipboard=False)
                  await ctx.send(download_link)
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)


    @commands.command()
    async def spoliste(self, ctx, url, quality = None):
       if quality == None:
          quality = "MP3_320"
       arl = await self.config.token()
       downloa = Login(arl) 
       downloa.download_playlistspo(
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
       for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                  download_link = send_to_transfersh(filepath, clipboard=False)
                  await ctx.send(download_link)
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)


    @commands.command()
    async def deezparça(self, ctx, url, quality = None):
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
                  download_link = send_to_transfersh(filepath, clipboard=False)
                  await ctx.send(download_link)
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)


    @commands.command()
    async def deezalbüm(self, ctx, url, quality = None):
       if quality == None:
          quality = "MP3_320"
       arl = await self.config.token()
       downloa = Login(arl) 
       downloa.download_albumdee(
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
       for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                  download_link = send_to_transfersh(filepath, clipboard=False)
                  await ctx.send(download_link)
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)


    @commands.command()
    async def deezliste(self, ctx, url, quality = None):
       if quality == None:
          quality = "MP3_320"
       arl = await self.config.token()
       downloa = Login(arl) 
       downloa.download_playlistdee(
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
       for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in [".zip"]:
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                  download_link = send_to_transfersh(filepath, clipboard=False)
                  await ctx.send(download_link)
       with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                   shutil.rmtree(entry.path)
                else:
                   os.remove(entry.path)
                
