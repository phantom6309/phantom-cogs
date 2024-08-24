import aiohttp
import discord
import json
import asyncio
from redbot.core import commands
from discord.ext import tasks

class Trakt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data.json'
        self.data = self.load_data()
        self.check_for_updates.start()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                'trakt_credentials': {},
                'tracked_users': {},
                'last_activity': {},
                'channel_id': None,
                'tmdb_api_key': None
            }
        if 'last_activity' not in data:
            data['last_activity'] = {}
        return data

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    async def get_trakt_user_activity(self, username, access_token):
        url = f'https://api.trakt.tv/users/{username}/history'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'trakt-api-version': '2',
            'trakt-api-key': self.data['trakt_credentials'].get('client_id')
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        # Handle and log errors
                        print(f"Failed to fetch activity for user {username}. Status code: {response.status}")
                        return None
        except Exception as e:
            print(f"Error fetching activity for user {username}: {e}")
            return None

    def extract_title(self, activity_item):
        if 'movie' in activity_item:
            return activity_item['movie']['title'], 'movie', None
        elif 'show' in activity_item:
            show_title = activity_item['show']['title']
            episode = activity_item.get('episode', {})
            season = episode.get('season', 'N/A')
            episode_number = episode.get('number', 'N/A')
            return show_title, 'show', (season, episode_number)
        return 'Unknown Title', 'unknown', None

    @commands.group(name='trakt', invoke_without_command=True)
    async def trakt(self, ctx):
        await ctx.send("Available commands: `user`, `setup`, `run`, `setupchannel`, `settmdbkey`")

    @trakt.command()
    async def setup(self, ctx):
        try:
            await ctx.author.send("Enter your Trakt Client ID:")
            client_id = await self.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel))
            client_id = client_id.content.strip()

            await ctx.author.send("Enter your Trakt Client Secret:")
            client_secret = await self.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel))
            client_secret = client_secret.content.strip()

            redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            oauth_url = f'https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
            await ctx.author.send(f"Authorize the application by visiting this URL: {oauth_url}\nAfter authorization, please send me the authorization code.")

            authorization_code = await self.bot.wait_for('message', timeout=300.0, check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel))
            authorization_code = authorization_code.content.strip()

            token_data = {
                'code': authorization_code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.trakt.tv/oauth/token', data=token_data) as response:
                    if response.status == 200:
                        token_response = await response.json()
                        access_token = token_response.get('access_token')
                        self.data['trakt_credentials'] = {
                            'client_id': client_id,
                            'client_secret': client_secret,
                            'access_token': access_token
                        }
                        self.save_data()
                        await ctx.author.send("Trakt credentials successfully set up.")
                    else:
                        await ctx.author.send(f"Failed to obtain access token: {await response.text()}")
        except asyncio.TimeoutError:
            await ctx.author.send("Response timed out. Please try the setup command again.")
        except Exception as e:
            await ctx.author.send(f"An error occurred: {e}")

    @trakt.command()
    async def settmdbkey(self, ctx, api_key: str):
        """Set or update TMDb API key."""
        self.data['tmdb_api_key'] = api_key
        self.save_data()
        await ctx.send("TMDb API key updated.")

    @trakt.command()
    async def user(self, ctx, username: str):
        if isinstance(self.data['tracked_users'], list):
            self.data['tracked_users'] = {user: {} for user in self.data['tracked_users']}
        
        if username in self.data['tracked_users']:
            del self.data['tracked_users'][username]
            self.data['last_activity'].pop(username, None)
            self.save_data()
            await ctx.send(f"User {username} removed from the tracking list.")
        else:
            self.data['tracked_users'][username] = {}
            self.save_data()
            await ctx.send(f"User {username} added to the tracking list.")

    @trakt.command()
    async def setupchannel(self, ctx, *, channel: discord.TextChannel):
        self.data['channel_id'] = channel.id
        self.save_data()
        await ctx.send(f"{channel.name} channel set for tracking.")

    async def create_embed_with_tmdb_info(self, title, content_type, episode_info=None):
     api_key = self.data.get('tmdb_api_key')
     if not api_key:
        return discord.Embed(title=title, description="TMDb API key not set.", color=discord.Color.red())

     if content_type == 'movie':
        url = f"https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}&language=tr-TR"
     else:  # content_type == 'show'
        url = f"https://api.themoviedb.org/3/search/tv?query={title}&api_key={api_key}&language=tr-TR"

     try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['results']:
                        item = data['results'][0]
                        embed_title = item.get('title' if content_type == 'movie' else 'name', title)
                        description = item.get('overview', 'No description available.')
                        if content_type == 'show' and episode_info:
                            season, episode_number = episode_info
                            description = f"{description}\n\nSeason {season} Episode {episode_number}"

                        embed = discord.Embed(
                            title=f"{embed_title} - {title}",
                            description=description,
                            color=discord.Color.blue()
                        )
                        embed.set_image(url=f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}")
                        embed.add_field(name="Rating", value=item.get('vote_average', 'N/A'), inline=True)
                        if content_type == 'show':
                            embed.add_field(name="Seasons", value=item.get('number_of_seasons', 'N/A'), inline=True)
                            embed.add_field(name="Episodes", value=item.get('number_of_episodes', 'N/A'), inline=True)
                        return embed
                    else:
                        return discord.Embed(title=title, description="No results found on TMDb.", color=discord.Color.red())
                else:
                    logger.error(f"Failed to fetch TMDb data. Status code: {response.status}")
                    return discord.Embed(title=title, description="Failed to fetch TMDb data.", color=discord.Color.red())
     except Exception as e:
        logger.error(f"Error fetching TMDb data: {e}")
        return discord.Embed(title=title, description="Error fetching TMDb data.", color=discord.Color.red())

    @tasks.loop(minutes=15)
    async def check_for_updates(self):
      await self.bot.wait_until_ready()
      if not self.data['trakt_credentials'].get('access_token'):
        return
      if not self.data['tracked_users']:
        return
      if not self.data.get('channel_id'):
        return

      channel = self.bot.get_channel(int(self.data['channel_id']))
      if not channel:
        logger.error("Channel not found.")
        return

      for username in self.data['tracked_users']:
        activity = await self.get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
        if activity:
            latest_activity = activity[0]
            title, content_type, episode_info = self.extract_title(latest_activity)
            last_watched = self.data['last_activity'].get(username)
            if last_watched != title:
                self.data['last_activity'][username] = title
                self.save_data()
                embed = await self.create_embed_with_tmdb_info(title, content_type, episode_info)
                if content_type == 'show' and episode_info:
                    embed.set_author(name=f"{username} watched", icon_url=None)
                    embed.set_footer(text=f"Season {episode_info[0]} Episode {episode_info[1]}", icon_url=None)
                else:
                    embed.set_author(name=f"{username} watched", icon_url=None)
                await channel.send(embed=embed)

