import aiohttp
import discord
import json
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
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    def extract_title(self, activity_item):
     if 'movie' in activity_item:
        return activity_item['movie']['title'], 'movie', None, None, None
     elif 'episode' in activity_item and 'show' in activity_item:
        show_title = activity_item['show']['title']
        episode_title = activity_item['episode']['title']
        season_number = activity_item['episode']['season']
        episode_number = activity_item['episode']['number']
        return f"{show_title} - {episode_title}", 'episode', show_title, season_number, episode_number
     elif 'show' in activity_item:
        return activity_item['show']['title'], 'show', None, None, None
     return 'Bilinmeyen Başlık', 'unknown', None, None, None
    
    @commands.group(name='trakt', invoke_without_command=True)
    async def trakt(self, ctx):
        await ctx.send("Mevcut komutlar: `user`, `setup`, `run`, `setupchannel`, `settmdbkey`")

    @trakt.command()
    async def setup(self, ctx):
        await ctx.author.send("Trakt Client ID'nizi girin:")
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
        
        try:
            # Trakt Client ID'yi al
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_id = msg.content.strip()
            
            # Trakt Client Secret'ı al
            await ctx.author.send("Trakt Client Secret'ınızı girin:")
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_secret = msg.content.strip()
            
            # Trakt için OAuth ayarı
            redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            oauth_url = f'https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
            await ctx.author.send(f"Uygulamayı yetkilendirmek için bu URL'yi ziyaret edin: {oauth_url}\nYetkilendirme sonrası, lütfen bana yetkilendirme kodunu gönderin.")
            
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
                        # Trakt kimlik bilgilerini kaydet
                        self.data['trakt_credentials'] = {
                            'client_id': client_id,
                            'client_secret': client_secret,
                            'access_token': access_token
                        }
                        self.save_data()
                        await ctx.author.send("Trakt kimlik bilgileri başarıyla ayarlandı.")
                    else:
                        await ctx.author.send(f"Erişim belirteci alınamadı: {await response.text()}")
        
        except asyncio.TimeoutError:
            await ctx.author.send("Yanıt vermek çok uzun sürdü. Lütfen setup komutunu tekrar deneyin.")
    
    @trakt.command()
    async def settmdbkey(self, ctx, api_key: str):
        """TMDb API anahtarını ayarlama veya güncelleme komutu."""
        self.data['tmdb_api_key'] = api_key
        self.save_data()
        await ctx.send("TMDb API anahtarı güncellendi.")

    @trakt.command()
    async def user(self, ctx, username: str):
        if isinstance(self.data['tracked_users'], list):
            self.data['tracked_users'] = {user: {} for user in self.data['tracked_users']}
        
        if username in self.data['tracked_users']:
            del self.data['tracked_users'][username]
            if username in self.data['last_activity']:
                del self.data['last_activity'][username]
            self.save_data()
            await ctx.send(f"Kullanıcı {username} takip listesinden kaldırıldı.")
        else:
            self.data['tracked_users'][username] = {}
            self.save_data()
            await ctx.send(f"Kullanıcı {username} takip listesine eklendi.")

    @trakt.command()
    async def run(self, ctx):
     if not self.data['trakt_credentials'].get('access_token'):
        await ctx.send("Trakt erişim belirteci bulunamadı. Öncelikle `?trakt setup` komutunu kullanarak kimlik bilgilerini ayarlayın.")
        return

     if not self.data['tracked_users']:
        await ctx.send("Takip edilecek kullanıcı bulunmuyor. Öncelikle `?trakt user <kullanıcı_adı>` komutunu kullanarak kullanıcı ekleyin.")
        return

     channel_id = self.data.get('channel_id')
     if channel_id is None:
        await ctx.send("Bir kanal ayarlanmamış. Kanalı ayarlamak için `?trakt setupchannel <kanal_id>` komutunu kullanın.")
        return

     channel = self.bot.get_channel(int(channel_id))
     if channel is None:
        await ctx.send("Geçersiz kanal ID'si. Kanalı tekrar ayarlamak için `?trakt setupchannel <kanal_id>` komutunu kullanın.")
        return

     for username in self.data['tracked_users']:
        activity = await self.get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
        if activity:
            latest_activity = activity[0]
            title, content_type, show_title = self.extract_title(latest_activity)
            last_watched = self.data['last_activity'].get(username)
            if last_watched != title:
                self.data['last_activity'][username] = title
                self.save_data()
                embed = await self.create_embed_with_tmdb_info(title, content_type, show_title)
                embed.set_author(name=username, icon_url=None)
                embed.set_footer(text=f"{username}", icon_url=None)
                await channel.send(embed=embed)
                
    async def create_embed_with_tmdb_info(self, title, content_type, show_title=None, season_number=None, episode_number=None):
     api_key = self.data.get('tmdb_api_key')
     if not api_key:
        return discord.Embed(title=title, description="TMDb API anahtarı ayarlanmamış.", color=discord.Color.red())

     if content_type == 'movie':
        url = f"https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}&language=tr-TR"
     elif content_type == 'show':
        url = f"https://api.themoviedb.org/3/search/tv?query={title}&api_key={api_key}&language=tr-TR"
     elif content_type == 'episode' and show_title:
        show_url = f"https://api.themoviedb.org/3/search/tv?query={show_title}&api_key={api_key}&language=tr-TR"
        async with aiohttp.ClientSession() as session:
            async with session.get(show_url) as response:
                if response.status == 200:
                    show_data = await response.json()
                    if show_data['results']:
                        show_id = show_data['results'][0]['id']
                        episode_url = f"https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}/episode/{episode_number}?api_key={api_key}&language=tr-TR"
                        async with session.get(episode_url) as episode_response:
                            if episode_response.status == 200:
                                episode_data = await episode_response.json()
                                embed = discord.Embed(
                                    title=episode_data.get('name', title),
                                    description=episode_data.get('overview', 'Açıklama bulunamadı.'),
                                    color=discord.Color.blue()
                                )
                                embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{episode_data.get('still_path')}")
                                embed.add_field(name="Sezon", value=season_number, inline=True)
                                embed.add_field(name="Bölüm", value=episode_number, inline=True)
                                embed.add_field(name="Puan", value=episode_data.get('vote_average', 'N/A'), inline=True)
                                embed.add_field(name="Çıkış Tarihi", value=episode_data.get('air_date', 'N/A'), inline=True)
                                embed.add_field(name="Tür", value=', '.join([genre['name'] for genre in episode_data.get('genres', [])]), inline=False)
                                return embed
                            else:
                                return discord.Embed(title=title, description="Episod bilgisi alınamadı.", color=discord.Color.red())
                    else:
                     return discord.Embed(title=title, description="Şov bilgisi alınamadı.", color=discord.Color.red())
                else:
                  return discord.Embed(title=title, description="Bilgi bulunamadı.", color=discord.Color.orange())
        


    @trakt.command()
    async def setupchannel(self, ctx, *, channel: discord.TextChannel):
        self.data['channel_id'] = channel.id
        self.save_data()
        await ctx.send(f"{channel.name} kanalı takip edilecek şekilde ayarlandı.")

    @tasks.loop(minutes=5)
    async def check_for_updates(self):
        if not self.data['trakt_credentials'].get('access_token'):
            return

        if not self.data['tracked_users']:
            return

        channel_id = self.data.get('channel_id')
        if channel_id is None:
            return

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            return

        for username in self.data['tracked_users']:
            activity = await self.get_trakt_user_activity(username, self.data['trakt_credentials'].get('access_token'))
            if activity:
                latest_activity = activity[0]
                title, content_type = self.extract_title(latest_activity)
                last_watched = self.data['last_activity'].get(username)
                if last_watched != title:
                    self.data['last_activity'][username] = title
                    self.save_data()
                    embed = await self.create_embed_with_tmdb_info(title, content_type)
                    embed.set_author(name=username, icon_url=None)
                    embed.set_footer(text=f"{username}", icon_url=None)
                    await channel.send(embed=embed)

    @check_for_updates.before_loop
    async def before_checking(self):
        await self.bot.wait_until_ready()
        
