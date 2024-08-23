import aiohttp
import discord
import json
from redbot.core import commands
from discord.ext import tasks
from googletrans import Translator

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
            data = {'trakt_credentials': {}, 'tracked_users': {}, 'last_activity': {}, 'channel_id': None, 'omdb_api_key': None}
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
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    def extract_title(self, activity_item):
        if 'movie' in activity_item:
            return activity_item['movie']['title']
        elif 'episode' in activity_item and 'show' in activity_item:
            return f"{activity_item['show']['title']} - {activity_item['episode']['title']}"
        elif 'show' in activity_item:
            return activity_item['show']['title']
        return 'Unknown Title'

    @commands.group(name='trakt', invoke_without_command=True)
    async def trakt(self, ctx):
        await ctx.send("Available commands: `user`, `setup`, `run`, `setupchannel`, `setomdbkey`")

    @trakt.command()
    async def setup(self, ctx):
        await ctx.author.send("Please provide your Trakt Client ID:")
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
        
        try:
            # Get Trakt Client ID
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_id = msg.content.strip()
            
            # Get Trakt Client Secret
            await ctx.author.send("Please provide your Trakt Client Secret:")
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_secret = msg.content.strip()
            
            # OAuth setup for Trakt
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
                        # Save Trakt credentials
                        self.data['trakt_credentials'] = {
                            'client_id': client_id,
                            'client_secret': client_secret,
                            'access_token': access_token
                        }
                        self.save_data()
                        await ctx.author.send("Trakt credentials have been set up successfully.")
                    else:
                        await ctx.author.send(f"Failed to get access token: {await response.text()}")
        
        except asyncio.TimeoutError:
            await ctx.author.send("You took too long to respond. Please try the setup command again.")
    
    @trakt.command()
    async def setomdbkey(self, ctx, api_key: str):
        """Command to set or update the OMDb API key."""
        self.data['omdb_api_key'] = api_key
        self.save_data()
        await ctx.send("OMDb API key has been updated.")

    @trakt.command()
    async def user(self, ctx, username: str):
        if isinstance(self.data['tracked_users'], list):
            self.data['tracked_users'] = {user: {} for user in self.data['tracked_users']}
        
        if username in self.data['tracked_users']:
            del self.data['tracked_users'][username]
            if username in self.data['last_activity']:
                del self.data['last_activity'][username]
            self.save_data()
            await ctx.send(f"User {username} has been removed from the tracking list.")
        else:
            self.data['tracked_users'][username] = {}
            self.save_data()
            await ctx.send(f"User {username} has been added to the tracking list.")

    @trakt.command()
    async def run(self, ctx):
     if not self.data['trakt_credentials'].get('access_token'):
        await ctx.send("Trakt erişim anahtarı bulunamadı. Lütfen önce `?trakt setup` komutunu kullanarak ayarlayın.")
        return
    
     if not self.data['tracked_users']:
        await ctx.send("İzlenecek kullanıcı yok. Lütfen önce `?trakt user <username>` komutunu kullanarak kullanıcı ekleyin.")
        return

     channel_id = self.data.get('channel_id')
     if channel_id is None:
        await ctx.send("Herhangi bir kanal ayarlanmadı. Lütfen `?trakt setupchannel <channel_id>` komutunu kullanarak kanalı ayarlayın.")
        return
    
     channel = self.bot.get_channel(int(channel_id))
     if channel is None:
        await ctx.send("Geçersiz kanal ID'si. Lütfen `?trakt setupchannel <channel_id>` komutunu kullanarak kanalı tekrar ayarlayın.")
        return

     for username in self.data['tracked_users']:
        activity = await self.get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
        if activity:
            latest_activity = activity[0]
            title = self.extract_title(latest_activity)
            last_watched = self.data['last_activity'].get(username)
            if last_watched != title:
                self.data['last_activity'][username] = title
                self.save_data()
                embed = await self.create_embed_with_omdb_info(title, username)
                await channel.send(embed=embed)
        else:
            await ctx.send(f'{username} için son etkinlik bulunamadı.')

    

    async def create_embed_with_omdb_info(self, title, username):
     api_key = self.data.get('omdb_api_key')
     if not api_key:
        return discord.Embed(title=title, description="OMDb API anahtarı ayarlanmadı.")

     url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
     async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                movie_data = await response.json()
                
                # Initialize the translator
                translator = Translator()

                # Translate fields to Turkish
                description = translator.translate(movie_data.get('Plot', 'Açıklama bulunamadı.'), dest='tr').text
                genre = translator.translate(movie_data.get('Genre', 'Tür bulunamadı.'), dest='tr').text

                embed = discord.Embed(
                    title=f"{movie_data.get('Title', title)} - {username} izledi",
                    description=description,
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=movie_data.get('Poster'))
                embed.add_field(name="Puan", value=movie_data.get('imdbRating', 'N/A'), inline=True)
                embed.add_field(name="Süre", value=movie_data.get('Runtime', 'N/A'), inline=True)
                embed.add_field(name="Tür", value=genre, inline=False)
                return embed
            else:
                return discord.Embed(title=title, description="OMDb'den ek bilgi alınamadı.")
                
    @trakt.command()
    async def setupchannel(self, ctx, *, channel: discord.TextChannel):
        self.data['channel_id'] = str(channel.id)
        self.save_data()
        await ctx.send(f"Channel ID has been set to {channel.mention}. This is where updates will be sent.")

    @tasks.loop(minutes=30)
    async def check_for_updates(self):
        if not self.data['trakt_credentials'].get('access_token') or not self.data['tracked_users']:
            return

        channel_id = self.data.get('channel_id')
        if channel_id is None:
            return
        
        channel = self.bot.get_channel(int(channel_id))
        if channel is none:
            print("Invalid channel ID. Please check your DISCORD_CHANNEL_ID.")
            return

        for username in self.data['tracked_users']:
            activity = await self.get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
            if activity:
                latest_activity = activity[0]
                title = self.extract_title(latest_activity)
                last_watched = self.data['last_activity'].get(username)
                if last_watched != title:
                    self.data['last_activity'][username] = title
                    self.save_data()
                    message = f'{username} watched {title}'
                    embed = await self.create_embed_with_omdb_info(title)
                    await channel.send(embed=embed)
                    