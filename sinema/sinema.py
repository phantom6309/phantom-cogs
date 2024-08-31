import discord
from redbot.core import commands, Config
import aiohttp

class Sinema(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=965854234)  # Replace with your own identifier
        default_global = {
            "api_key": None,
            "channel_id": None,
            "posted_movies": []
        }
        self.config.register_global(**default_global)

    @commands.group()
    async def sinema(self, ctx):
        """Commands related to movie updates."""
        pass

    @sinema.command()
    async def set_api_key(self, ctx, api_key: str):
        """Set the TMDb API key."""
        await self.config.api_key.set(api_key)
        await ctx.send("TMDb API key has been set.")

    @sinema.command()
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel where movie updates will be posted."""
        await self.config.channel_id.set(channel.id)
        await ctx.send(f"Channel set to {channel.mention} for movie updates.")

    @sinema.command()
    async def now_playing(self, ctx):
        """Fetches and displays movies currently playing in Turkish cinemas."""
        await self.post_new_movies()

    @sinema.command()
    async def clear_posted(self, ctx):
        """Clear the list of already posted movies."""
        await self.config.posted_movies.set([])
        await ctx.send("Posted movies list has been cleared.")

    async def post_new_movies(self):
        api_key = await self.config.api_key()
        channel_id = await self.config.channel_id()
        posted_movies = await self.config.posted_movies()

        if not api_key or not channel_id:
            return  # No API key or channel set

        url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=tr-TR"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        movies = data.get("results", [])
        channel = self.bot.get_channel(channel_id)

        if not channel:
            return  # Channel not found

        new_posted_movies = []

        for movie in movies:
            movie_id = movie['id']
            if movie_id in posted_movies:
                continue  # Skip movies already posted

            # Create an embed for each movie
            embed = discord.Embed(
                title=movie['title'],
                description=movie.get('overview', 'No description available.'),
                color=discord.Color.blue()
            )
            embed.add_field(name="Rating", value=movie.get('vote_average', 'N/A'), inline=True)
            embed.add_field(name="Release Date", value=movie.get('release_date', 'N/A'), inline=True)
            embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}")

            await channel.send(embed=embed)
            new_posted_movies.append(movie_id)

        # Update the list of posted movies
        await self.config.posted_movies.set(posted_movies + new_posted_movies)

def setup(bot):
    bot.add_cog(Sinema(bot))
    
