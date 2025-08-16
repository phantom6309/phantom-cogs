import aiohttp
import discord
import json
import asyncio
import os
import logging
from redbot.core import commands, Config
from discord.ext import tasks
from urllib.parse import quote_plus

log = logging.getLogger("red.trakt")

class Trakt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Use Red's config system instead of direct file access
        self.config = Config.get_conf(self, identifier=1234567891, force_registration=True)
        
        default_global = {
            'trakt_credentials': {},
            'tracked_users': {},
            'last_activity': {},
            'channel_id': None,
            'tmdb_api_key': None
        }
        
        self.config.register_global(**default_global)
        self.check_for_updates.start()

    def cog_unload(self):
        """Clean up when cog is unloaded"""
        self.check_for_updates.cancel()

    async def get_trakt_user_activity(self, username, access_token, client_id):
        url = f'https://api.trakt.tv/users/{username}/history'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'trakt-api-version': '2',
            'trakt-api-key': client_id
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        log.error(f"Failed to fetch activity for user {username}. Status code: {response.status}")
                        if response.status == 401:
                            log.error("Access token may be expired or invalid")
                        return None
        except Exception as e:
            log.error(f"Error fetching activity for user {username}: {e}")
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
    @commands.is_owner()
    async def trakt(self, ctx):
        """Trakt.tv integration commands"""
        await ctx.send("Available commands: `user`, `setup`, `setupchannel`, `settmdbkey`, `status`, `test`")

    @trakt.command()
    @commands.is_owner()
    async def setup(self, ctx):
        """Setup Trakt credentials via OAuth"""
        try:
            await ctx.author.send("📝 **Trakt Setup Process Started**\n\nEnter your Trakt Client ID:")
            
            def check(m):
                return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
            
            client_id_msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_id = client_id_msg.content.strip()

            await ctx.author.send("Enter your Trakt Client Secret:")
            client_secret_msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_secret = client_secret_msg.content.strip()

            redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            oauth_url = f'https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
            
            embed = discord.Embed(
                title="🔐 Authorization Required",
                description=f"[Click here to authorize the application]({oauth_url})\n\nAfter authorization, please send me the authorization code.",
                color=discord.Color.blue()
            )
            await ctx.author.send(embed=embed)

            auth_code_msg = await self.bot.wait_for('message', timeout=300.0, check=check)
            authorization_code = auth_code_msg.content.strip()

            # Exchange authorization code for access token
            token_data = {
                'code': authorization_code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.trakt.tv/oauth/token', json=token_data) as response:
                    if response.status == 200:
                        token_response = await response.json()
                        access_token = token_response.get('access_token')
                        refresh_token = token_response.get('refresh_token')
                        
                        credentials = {
                            'client_id': client_id,
                            'client_secret': client_secret,
                            'access_token': access_token,
                            'refresh_token': refresh_token
                        }
                        
                        await self.config.trakt_credentials.set(credentials)
                        
                        embed = discord.Embed(
                            title="✅ Setup Complete",
                            description="Trakt credentials successfully configured!",
                            color=discord.Color.green()
                        )
                        await ctx.author.send(embed=embed)
                    else:
                        error_text = await response.text()
                        log.error(f"Token exchange failed: {error_text}")
                        await ctx.author.send(f"❌ Failed to obtain access token: {error_text}")
                        
        except asyncio.TimeoutError:
            await ctx.author.send("⏰ Response timed out. Please try the setup command again.")
        except Exception as e:
            log.error(f"Setup error: {e}")
            await ctx.author.send(f"❌ An error occurred: {e}")

    @trakt.command()
    @commands.is_owner()
    async def settmdbkey(self, ctx, api_key: str):
        """Set or update TMDb API key"""
        await self.config.tmdb_api_key.set(api_key)
        await ctx.send("✅ TMDb API key updated.")

    @trakt.command()
    @commands.is_owner()
    async def user(self, ctx, username: str):
        """Add or remove a user from tracking"""
        tracked_users = await self.config.tracked_users()
        
        if username in tracked_users:
            del tracked_users[username]
            await self.config.tracked_users.set(tracked_users)
            
            # Also remove from last_activity
            last_activity = await self.config.last_activity()
            last_activity.pop(username, None)
            await self.config.last_activity.set(last_activity)
            
            await ctx.send(f"❌ User **{username}** removed from tracking.")
        else:
            tracked_users[username] = {}
            await self.config.tracked_users.set(tracked_users)
            await ctx.send(f"✅ User **{username}** added to tracking.")

    @trakt.command()
    @commands.is_owner()
    async def setupchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel for activity notifications"""
        await self.config.channel_id.set(channel.id)
        await ctx.send(f"✅ Activity notifications will be sent to {channel.mention}")

    @trakt.command()
    @commands.is_owner()
    async def status(self, ctx):
        """Show current configuration status"""
        credentials = await self.config.trakt_credentials()
        channel_id = await self.config.channel_id()
        tmdb_key = await self.config.tmdb_api_key()
        tracked_users = await self.config.tracked_users()
        
        embed = discord.Embed(title="🔧 Trakt Configuration Status", color=discord.Color.blue())
        
        # Trakt API status
        if credentials.get('access_token'):
            embed.add_field(name="Trakt API", value="✅ Configured", inline=True)
        else:
            embed.add_field(name="Trakt API", value="❌ Not configured", inline=True)
        
        # TMDb API status
        if tmdb_key:
            embed.add_field(name="TMDb API", value="✅ Configured", inline=True)
        else:
            embed.add_field(name="TMDb API", value="❌ Not configured", inline=True)
        
        # Channel status
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed.add_field(name="Notification Channel", value=f"✅ {channel.mention}", inline=True)
            else:
                embed.add_field(name="Notification Channel", value="❌ Channel not found", inline=True)
        else:
            embed.add_field(name="Notification Channel", value="❌ Not set", inline=True)
        
        # Tracked users
        if tracked_users:
            user_list = ", ".join(tracked_users.keys())
            embed.add_field(name="Tracked Users", value=user_list, inline=False)
        else:
            embed.add_field(name="Tracked Users", value="None", inline=False)
        
        await ctx.send(embed=embed)

    @trakt.command()
    @commands.is_owner()
    async def test(self, ctx, username: str):
        """Test fetching activity for a specific user"""
        credentials = await self.config.trakt_credentials()
        
        if not credentials.get('access_token'):
            await ctx.send("❌ Trakt credentials not configured. Run `trakt setup` first.")
            return
        
        activity = await self.get_trakt_user_activity(
            username, 
            credentials.get('access_token'),
            credentials.get('client_id')
        )
        
        if activity:
            latest_activity = activity[0]
            title, content_type, episode_info = self.extract_title(latest_activity)
            embed = await self.create_embed_with_tmdb_info(username, title, content_type, episode_info)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Could not fetch activity for user **{username}**")

    async def create_embed_with_tmdb_info(self, username, title, content_type, episode_info=None):
        api_key = await self.config.tmdb_api_key()
        if not api_key:
            embed = discord.Embed(
                title=f"{username} watched {title}",
                description="TMDb API key not configured for additional info.",
                color=discord.Color.orange()
            )
            return embed

        # URL encode the title for the API request
        encoded_title = quote_plus(title)
        
        if content_type == 'movie':
            url = f"https://api.themoviedb.org/3/search/movie?query={encoded_title}&api_key={api_key}&language=en-US"
        else:  # content_type == 'show'
            url = f"https://api.themoviedb.org/3/search/tv?query={encoded_title}&api_key={api_key}&language=en-US"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['results']:
                            item = data['results'][0]
                            
                            if content_type == 'movie':
                                embed_title = f"🎬 {username} watched {item.get('title', title)}"
                            else:
                                show_name = item.get('name', title)
                                if episode_info and episode_info[0] != 'N/A' and episode_info[1] != 'N/A':
                                    season, episode_number = episode_info
                                    embed_title = f"📺 {username} watched {show_name} S{season}E{episode_number}"
                                else:
                                    embed_title = f"📺 {username} watched {show_name}"

                            description = item.get('overview', 'No description available.')
                            if len(description) > 300:
                                description = description[:297] + "..."

                            embed = discord.Embed(
                                title=embed_title,
                                description=description,
                                color=discord.Color.blue()
                            )
                            
                            # Add poster image if available
                            if item.get('poster_path'):
                                embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w300{item.get('poster_path')}")
                            
                            # Add rating
                            rating = item.get('vote_average', 'N/A')
                            if rating != 'N/A':
                                embed.add_field(name="⭐ Rating", value=f"{rating}/10", inline=True)
                            
                            # Add release/air date
                            if content_type == 'movie':
                                release_date = item.get('release_date', 'N/A')
                                if release_date != 'N/A':
                                    embed.add_field(name="📅 Release Date", value=release_date, inline=True)
                            else:
                                first_air_date = item.get('first_air_date', 'N/A')
                                if first_air_date != 'N/A':
                                    embed.add_field(name="📅 First Aired", value=first_air_date, inline=True)
                                
                                # Add season/episode info for shows
                                if episode_info and episode_info[0] != 'N/A' and episode_info[1] != 'N/A':
                                    season, episode_number = episode_info
                                    embed.add_field(name="📺 Episode", value=f"Season {season}, Episode {episode_number}", inline=True)
                            
                            return embed
                        else:
                            embed = discord.Embed(
                                title=f"{username} watched {title}",
                                description="No additional info found on TMDb.",
                                color=discord.Color.orange()
                            )
                            return embed
                    else:
                        log.error(f"Failed to fetch TMDb data. Status code: {response.status}")
                        embed = discord.Embed(
                            title=f"{username} watched {title}",
                            description="Failed to fetch additional info from TMDb.",
                            color=discord.Color.orange()
                        )
                        return embed
        except Exception as e:
            log.error(f"Error fetching TMDb data: {e}")
            embed = discord.Embed(
                title=f"{username} watched {title}",
                description="Error fetching additional info from TMDb.",
                color=discord.Color.orange()
            )
            return embed

    @tasks.loop(minutes=240)
    async def check_for_updates(self):
        await self.bot.wait_until_ready()
        
        try:
            credentials = await self.config.trakt_credentials()
            tracked_users = await self.config.tracked_users()
            channel_id = await self.config.channel_id()
            
            if not credentials.get('access_token'):
                return
            if not tracked_users:
                return
            if not channel_id:
                return

            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                log.error("Configured channel not found.")
                return

            last_activity = await self.config.last_activity()
            
            for username in tracked_users:
                try:
                    activity = await self.get_trakt_user_activity(
                        username, 
                        credentials.get('access_token'),
                        credentials.get('client_id')
                    )
                    
                    if activity:
                        latest_activity = activity[0]
                        title, content_type, episode_info = self.extract_title(latest_activity)
                        
                        # Create a unique identifier for this activity
                        activity_id = f"{title}_{latest_activity.get('watched_at', '')}"
                        last_activity_id = last_activity.get(username)
                        
                        if last_activity_id != activity_id:
                            # Update last activity
                            last_activity[username] = activity_id
                            await self.config.last_activity.set(last_activity)
                            
                            # Create and send embed
                            embed = await self.create_embed_with_tmdb_info(username, title, content_type, episode_info)
                            await channel.send(embed=embed)
                            
                            log.info(f"Posted activity for {username}: {title}")
                            
                except Exception as e:
                    log.error(f"Error processing user {username}: {e}")
                    
        except Exception as e:
            log.error(f"Error in check_for_updates: {e}")

    @check_for_updates.before_loop
    async def before_check_for_updates(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Trakt(bot))
