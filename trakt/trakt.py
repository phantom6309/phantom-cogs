import requests
import discord
import json
import asyncio
from discord.ext import commands, tasks

class Trakt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data.json'
        self.data = self.load_data()
        self.check_for_updates.start()

    # Load data from file
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'trakt_credentials': {}, 'tracked_users': {}, 'last_activity': {}, 'channel_id': None}
        # Ensure last_activity key is present
        if 'last_activity' not in data:
            data['last_activity'] = {}
        return data

    # Save data to file
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    # Function to get user activity from Trakt
    def get_trakt_user_activity(self, username, access_token):
        url = f'https://api.trakt.tv/users/{username}/history'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'trakt-api-version': '2',
            'trakt-api-key': self.data['trakt_credentials'].get('client_id')
        }
        response = requests.get(url, headers=headers)
        return response.json()

    # Function to extract title from activity item
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
        await ctx.send("Available commands: `user`, `setup`, `run`, `setupchannel`")

    @trakt.command()
    async def user(self, ctx, username: str):
        # Convert tracked_users list to a dictionary if necessary
        if isinstance(self.data['tracked_users'], list):
            self.data['tracked_users'] = {user: {} for user in self.data['tracked_users']}
        
        if username in self.data['tracked_users']:
            # Remove the user
            del self.data['tracked_users'][username]
            if username in self.data['last_activity']:
                del self.data['last_activity'][username]
            self.save_data()
            await ctx.send(f"User {username} has been removed from the tracking list.")
        else:
            # Add the user
            self.data['tracked_users'][username] = {}
            self.save_data()
            await ctx.send(f"User {username} has been added to the tracking list.")

    @trakt.command()
    async def setup(self, ctx):
        # Ask user for client ID and secret in DM
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

            # Exchange the authorization code for an access token
            token_data = {
                'code': authorization_code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            response = requests.post('https://api.trakt.tv/oauth/token', data=token_data)
            
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                self.data['trakt_credentials'] = {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'access_token': access_token
                }
                self.save_data()
                await ctx.author.send("Trakt credentials and access token have been set up successfully.")
            else:
                await ctx.author.send(f"Failed to get access token: {response.json()}")
        
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
            activity = self.get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
            if activity:
                latest_activity = activity[0]
                title = self.extract_title(latest_activity)
                last_watched = self.data['last_activity'].get(username)
                if last_watched != title:
                    self.data['last_activity'][username] = title
                    self.save_data()
                    message = f'{username} watched {title}'
                    await ctx.send(message)
            else:
                await ctx.send(f'No recent activity found for {username}.')

    @trakt.command()
    async def setupchannel(self, ctx, channel_id: int):
        # Set the channel ID
        self.data['channel_id'] = str(channel_id)
        self.save_data()
        await ctx.send(f"Channel ID has been set to {channel_id}. This is where updates will be sent.")

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
            activity = self.get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
            if activity:
                latest_activity = activity[0]
                title = self.extract_title(latest_activity)
                last_watched = self.data['last_activity'].get(username)
                if last_watched != title:
                    self.data['last_activity'][username] = title
                    self.save_data()
                    message = f'{username} watched {title}'
                    await channel.send(message)


      
