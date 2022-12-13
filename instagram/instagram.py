from redbot.core import commands
import discord
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Instagram(commands.Cog):
    """İnstagram video download"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def download_instagram_video(ctx, instagram_url):
  # Use BeautifulSoup to parse the HTML of the Instagram page
     soup = BeautifulSoup(urlopen(instagram_url), "html.parser")

  # Find the video URL in the page
     video_url = soup.find("meta", property="og:video")["content"]

  # Download the video data from the URL
     video_data = urlopen(video_url).read()

  # Create a new Discord file object from the video data
     video_file = discord.File(video_data, filename="video.mp4")

  # Post the video in the channel
     await ctx.send(file=video_file)
  
  # Delete the video data from the device
     video_data.delete()