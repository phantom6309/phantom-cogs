import discord
from redbot.core import commands
from discord.ext import tasks
from .utils.trakt_utils import get_trakt_user_activity, extract_title_and_imdb_id, get_imdb_info
from .utils.data_manager import load_data, save_data

class Trakt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data.json'
        self.data = load_data(self.data_file)
        self.check_for_updates.start()

    @commands.group(name='trakt', invoke_without_command=True)
    async def trakt(self, ctx):
        await ctx.send("Available commands: `user`, `setup`, `run`, `setupchannel`")

    @trakt.command()
    async def user(self, ctx, username: str):
        if isinstance(self.data['tracked_users'], list):
            self.data['tracked_users'] = {user: {} for user in self.data['tracked_users']}
        
        if username in self.data['tracked_users']:
            del self.data['tracked_users'][username]
            if username in self.data['last_activity']:
                del self.data['last_activity'][username]
            save_data(self.data_file, self.data)
            await ctx.send(f"User {username} has been removed from the tracking list.")
        else:
            self.data['tracked_users'][username] = {}
            save_data(self.data_file, self.data)
            await ctx.send(f"User {username} has been added to the tracking list.")

    @trakt.command()
    async def setup(self, ctx):
        await ctx.author.send("Please provide your Trakt Client ID:")
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
        
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_id = msg.content.strip()
            
            await ctx.author.send("Please provide your Trakt Client Secret:")
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_secret = msg.content.strip()
            
            redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            oauth_url = f'https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
            await ctx.author.send(f"Please authorize the application by visiting this URL: {oauth_url}\nAfter authorization, please send me the authorization code.")
            
            msg = await self.bot.wait_for('message', timeout=300.0, check=check)
            authorization_code = msg.content.strip()

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
                        save_data(self.data_file, self.data)
                        await ctx.author.send("Trakt credentials and access token have been set up successfully.")
                    else:
                        await ctx.author.send(f"Failed to get access token: {await response.text()}")
        
        except asyncio.TimeoutError:
            await ctx.author.send("You took too long to respond. Please try the setup command again.")

    @trakt.command()
    async def run(self, ctx):
        if not self.data['trakt_credentials'].get('access_token'):
            await ctx.send("No Trakt access token found. Please set up the credentials first using `?trakt setup`.")
            return
        
        if not self.data['tracked_users']:
            await ctx.send("No users to track. Please add users first using `?trakt user <username>`.")
            return

        channel_id = self.data.get('channel_id')
        if channel_id is None:
            await ctx.send("No channel has been set up. Please set the channel using `?trakt setupchannel <channel_id>`.")
            return
        
        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            await ctx.send("Invalid channel ID. Please set the channel again using `?trakt setupchannel <channel_id>`.")
            return

        for username in self.data['tracked_users']:
            activity = await get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
            if activity:
                latest_activity = activity[0]
                title, imdb_id = extract_title_and_imdb_id(latest_activity)
                last_watched = self.data['last_activity'].get(username)
                if last_watched != title:
                    self.data['last_activity'][username] = title
                    save_data(self.data_file, self.data)

                    # Fetch IMDb info
                    imdb_info = None
                    if imdb_id:
                        imdb_info = await get_imdb_info(imdb_id)

                    # Create embed message
                    embed = discord.Embed(title=title, description=f"{username} watched {title}", color=discord.Color.blue())
                    
                    if imdb_info:
                        embed.set_thumbnail(url=imdb_info['poster'])
                        embed.add_field(name="Plot", value=imdb_info['plot'], inline=False)
                        embed.add_field(name="Year", value=imdb_info['year'], inline=True)
                        embed.add_field(name="Genres", value=imdb_info['genres'], inline=True)
                        embed.add_field(name="Rating", value=imdb_info['rating'], inline=True)
                        embed.add_field(name="IMDB ID", value=f"[{imdb_id}](https://www.imdb.com/title/{imdb_id}/)")

                    await channel.send(embed=embed)
            else:
                await ctx.send(f'No recent activity found for {username}.')

    @trakt.command()
    async def setupchannel(self, ctx, *, channel: discord.TextChannel):
        self.data['channel_id'] = str(channel.id)
        save_data(self.data_file, self.data)
        await ctx.send(f"Channel ID has been set to {channel.mention}. This is where updates will be sent.")

    @tasks.loop(minutes=30)
    async def check_for_updates(self):
        if not self.data['trakt_credentials'].get('access_token') or not self.data['tracked_users']:
            return

        channel_id = self.data.get('channel_id')
        if channel_id is None:
            return
        
        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            print("Invalid channel ID. Please check your DISCORD_CHANNEL_ID.")
            return

        for username in self.data['tracked_users']:
            activity = await get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
            if activity:
                latest_activity = activity[0]
                title, imdb_id = extract_title_and_imdb_id(latest_activity)
                last_watched = self.data['last_activity'].get(username)
                if last_watched != title:
                    self.data['last_activity'][username] = title
                    save_data(self.data_file, self.data)

                    # Fetch IMDb info
                    imdb_info = None
                    if imdb_id:
                        imdb_info = await get_imdb_info(imdb_id)

                    # Create embed message
                    embed = discord.Embed(title=title, description=f"{username} watched {title}", color=discord.Color.blue())
                    
                    if imdb_info:
                        embed.set_thumbnail(url=imdb_info['poster'])
                        embed.add_field(name="Plot", value=imdb_info['plot'], inline=False)
                        embed.add_field(name="Year", value=imdb_info['year'], inline=True)
                        embed.add_field(name="Genres", value=imdb_info['genres'], inline=True)
                        embed.add_field(name="Rating", value=imdb_info['rating'], inline=True)
                        embed.add_field(name="IMDB ID", value=f"[{imdb_id}](https://www.imdb.com/title/{imdb_id}/)")

                    await channel.send(embed=embed)
            
