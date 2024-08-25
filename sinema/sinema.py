import discord
from discord.ext import tasks
from redbot.core import commands, Config
import http.client
import json

class Sinema(commands.Cog):
    """A cog that checks for upcoming movies and posts them to a Discord channel."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_global = {
            "api_key": None,
            "posted_movies": [],
            "channel_id": None
        }
        self.config.register_global(**default_global)
        self.check_movies.start()

    def cog_unload(self):
        self.check_movies.cancel()

    @commands.command()
    async def setapikey(self, ctx, api_key: str):
        """Set the API key for the movie API."""
        await self.config.api_key.set(api_key)
        await ctx.send("API key has been set.")

    @commands.command()
    async def setchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel where movie updates will be posted."""
        await self.config.channel_id.set(channel.id)
        await ctx.send(f"Channel has been set to {channel.mention}.")

    @commands.command()
    async def checkmovies(self, ctx):
        """Manually check for upcoming movies."""
        await self.check_and_post_movies(ctx)

    @tasks.loop(hours=24)
    async def check_movies(self):
        await self.check_and_post_movies()

    async def check_and_post_movies(self, ctx=None):
        api_key = await self.config.api_key()
        channel_id = await self.config.channel_id()

        if not api_key:
            if ctx:
                await ctx.send("API key is not set.")
            return

        if not channel_id:
            if ctx:
                await ctx.send("Channel is not set.")
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            if ctx:
                await ctx.send("Invalid channel.")
            return

        conn = http.client.HTTPSConnection("api.collectapi.com")
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"apikey {api_key}"
        }
        conn.request("GET", "/watching/moviesComing", headers=headers)
        res = conn.getresponse()
        data = res.read()
        movies_data = json.loads(data.decode("utf-8"))

        if movies_data.get("success"):
            posted_movies = await self.config.posted_movies()
            new_movies = []

            for movie in movies_data["result"]:
                if movie['name'] not in posted_movies:
                    embed = discord.Embed(
                        title=movie['name'],
                        description=movie['summary'],
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Type", value=movie['type'])
                    embed.set_image(url=movie['image'])
                    await channel.send(embed=embed)
                    new_movies.append(movie['name'])

            # Update the list of posted movies
            if new_movies:
                posted_movies.extend(new_movies)
                await self.config.posted_movies.set(posted_movies)
                if ctx:
                    await ctx.send(f"Posted {len(new_movies)} new movie(s).")
            else:
                if ctx:
                    await ctx.send("No new movies found.")
        else:
            if ctx:
                await ctx.send("Failed to retrieve movie data.")

    @check_movies.before_loop
    async def before_check_movies(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MovieNotifier(bot))
                  
