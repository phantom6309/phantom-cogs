import aiohttp
import discord
from redbot.core import commands, Config
from discord.ext import tasks

class Sinema(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=965854345)
        default_global = {
            "api_key": None,
            "posted_movies": [],  # List to store already posted movies
            "channel_id": None  # Channel ID where movies will be posted
        }
        self.config.register_global(**default_global)
        self.daily_task.start()  # Start the daily task

    def cog_unload(self):
        self.daily_task.cancel()  # Cancel the task when the cog is unloaded

    @tasks.loop(hours=24)
    async def daily_task(self):
        """Task to run daily and post new movies."""
        await self.post_new_movies()

    @daily_task.before_loop
    async def before_daily_task(self):
        """Wait until the bot is ready before starting the daily task."""
        await self.bot.wait_until_ready()

    async def post_new_movies(self):
        """Fetch and post new movies."""
        api_key = await self.config.api_key()
        if not api_key:
            return

        channel_id = await self.config.channel_id()
        if not channel_id:
            return
        
        url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=tr-TR&region=TR"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return
                
                data = await response.json()
                movies = data.get('results', [])
                
                if not movies:
                    return
                
                posted_movies = await self.config.posted_movies()
                new_movies = [movie for movie in movies if movie['id'] not in posted_movies]
                
                if not new_movies:
                    return
                
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    return
                
                embed = self._create_embed(new_movies)
                await channel.send(embed=embed)
                
                # Update the posted_movies list
                posted_movies.extend([movie['id'] for movie in new_movies])
                await self.config.posted_movies.set(posted_movies)

    def _create_embed(self, movies):
        embed = discord.Embed(title="Şu Anda Sinemalarda", color=discord.Color.blue())
        for movie in movies[:5]:  # Display the first 5 movies
            title = movie.get('title')
            release_date = movie.get('release_date')
            overview = movie.get('overview', 'Açıklama yok')
            rating = movie.get('vote_average', 'Puan yok')
            poster_path = movie.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            
            embed.add_field(
                name=f"{title} ({release_date})",
                value=f"Puan: {rating}\n\n{overview[:200]}...",
                inline=False
            )
            
            if poster_url:
                embed.set_image(url=poster_url)
        
        return embed

    @commands.group()
    async def sinema(self, ctx):
        """Group command for TMDb related commands."""
        pass

    @sinema.command()
    async def set_key(self, ctx, api_key: str):
        """Set the TMDb API key."""
        if len(api_key) != 32:  # Basic length check for the API key
            await ctx.send("Invalid API key. Please check and try again.")
            return
        
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

def setup(bot):
    bot.add_cog(Sinema(bot))
    
