import discord
from redbot import commands
from discord.ext import tasks
import json
import http.client

class Sinema(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_movies.start()

    def cog_unload(self):
        self.check_movies.cancel()

    @commands.group(name="sinema", invoke_without_command=True)
    async def sinema(self, ctx):
        await ctx.send("Available subcommands: `setapikey`, `setchannel`, `checkmovies`")

    @sinema.command(name="setapikey")
    async def set_api_key(self, ctx, api_key: str):
        await self.config.api_key.set(api_key)
        await ctx.send("API key has been set.")

    @sinema.command(name="setchannel")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        await self.config.channel_id.set(channel.id)
        await ctx.send(f"Channel set to {channel.mention}")

    @sinema.command(name="checkmovies")
    async def checkmovies(self, ctx):
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

        # Debugging: Print response status and raw data
        print(f"Response Status: {res.status}")
        data = res.read()
        print(f"Raw Data: {data}")

        if res.status != 200:
            if ctx:
                await ctx.send(f"API request failed with status code {res.status}.")
            return

        if not data:
            if ctx:
                await ctx.send("Received an empty response from the API.")
            return

        try:
            movies_data = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as e:
            if ctx:
                await ctx.send(f"Failed to decode the JSON response: {str(e)}")
            return

        if movies_data.get("success"):
            posted_movies = await self.config.posted_movies()
            new_movies = []

            for movie in movies_data.get("result", []):
                movie_name = movie.get('name')
                if movie_name and movie_name not in posted_movies:
                    embed = discord.Embed(
                        title=movie_name,
                        description=movie.get('summary', 'No summary available.'),
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Director", value=movie.get('director', 'Unknown'))
                    embed.add_field(name="Type", value=movie.get('type', 'Unknown'))
                    embed.set_image(url=movie.get('image', ''))

                    await channel.send(embed=embed)
                    new_movies.append(movie_name)

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

            
