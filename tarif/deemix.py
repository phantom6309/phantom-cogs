# -*- coding: utf-8 -*-
import discord
from redbot.core import checks, commands, bot





from pydeezer import Deezer, Downloader

from pydeezer.constants import track_formats

class Deezer(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.deezer = Deezer() # Create a Deezer object

        

    @commands.command()

    async def download(self, ctx, track_id):

        """Download a track and send it to the channel"""

        # Get information about the track

        track = self.deezer.get_track(track_id)

        track_info = track["info"]

        

        # Download the track

        download_dir = "downloads/"

        track["download"](download_dir, quality=track_formats.MP3_320)

        

        # Send the track to the channel

        with open(download_dir + track_info["title"] + ".mp3", "rb") as f:

            file = discord.File(f)

            await ctx.send(file=file)

    

    @commands.command()

    async def download_album(self, ctx, album_id):

        """Download all tracks in an album and send them to the channel"""

        # Get information about the album

        album = self.deezer.get_album(album_id)

        album_title = album["title"]

        tracks = album["tracks"]["data"]

        

        # Download the tracks

        download_dir = "downloads/"

        list_of_ids = [str(track["id"]) for track in tracks]

        downloader = Downloader(self.deezer, list_of_ids, download_dir,

                                quality=track_formats.MP3_320, concurrent_downloads=2)

        downloader.start()

        

        # Send the tracks to the channel

        for track in tracks:

            with open(download_dir + track["title"] + ".mp3", "rb") as f:

                file = discord.File(f)

                await ctx.send(file=file)

    

    @commands.command()

    async def download_playlist(self, ctx, playlist_id):

        """Download all tracks in a playlist and send them to the channel"""

        # Get information about the playlist

        playlist = self.deezer.get_playlist(playlist_id)

        playlist_title = playlist["title"]

        tracks = playlist["tracks"]["data"]

        

        # Download the tracks

        download_dir = "downloads/"

        list_of_ids = [str(track["id"]) for track in tracks]

        downloader = Downloader(self.deezer, list_of_ids, download_dir,

                                quality=track_formats.MP3_320, concurrent_downloads=2)

        downloader.start()

        

        # Send the tracks to the channel

        for track in tracks:

            with open(download_dir + track["title"] + ".mp3", "rb") as f:

                file = discord.File(f)

                await ctx.send(file=file)

