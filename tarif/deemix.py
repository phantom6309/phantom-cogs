# -*- coding: utf-8 -*-

from redbot.core import commands
from pydeezer import Deezer, Downloader
from pydeezer.constants import track_formats
from redbot.core.data_manager import cog_data_path

deezer = Deezer()

class Deemix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search_track')
    async def download(self, ctx, *search_query):
        query = ' '.join(search_query)
        search_results = deezer.search_tracks(query)
        
        if len(search_results) == 0:
            await ctx.send("No search results found.")
            return
        
        track = search_results[0]
        track_id = track["info"]["ID"]
        track_name = track["info"]["title"]
        download_dir = cog_data_path(self)
        downloader = Downloader(deezer, [track_id], download_dir,
                                quality=track_formats.FLAC, concurrent_downloads=2)
        downloader.start()
        filename = f"{track_name}.mp3"
        fp = cog_data_path(self) / filename
        file = discord.File(str(fp), filename=filename)
        try:
           await ctx.send(files=[file])
        except Exception:
             log.error("Error sending song", exc_info=True)
              pass
        try:
              os.remove(fp)
        except Exception:
             log.error("Error deleting song", exc_info=True)

