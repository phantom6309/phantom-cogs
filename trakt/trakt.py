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
            data = {'trakt_credentials': {}, 'tracked_users': {}, 'last_activity': {}, 'channel_id': None, 'tmdb_api_key': None}
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
            return activity_item['movie']['title'], 'movie'
        elif 'episode' in activity_item and 'show' in activity_item:
            return f"{activity_item['show']['title']} - {activity_item['episode']['title']}", 'series'
        elif 'show' in activity_item:
            return activity_item['show']['title'], 'series'
        return 'Bilinmeyen Başlık', 'unknown'

    @commands.group(name='trakt', invoke_without_command=True)
    async def trakt(self, ctx):
        await ctx.send("Mevcut komutlar: `user`, `setup`, `run`, `setupchannel`, `settmdbkey`")

    @trakt.command()
    async def setup(self, ctx):
        await ctx.author.send("Lütfen Trakt Client ID'nizi girin:")
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        try:
            # Get Trakt Client ID
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_id = msg.content.strip()

            # Get Trakt Client Secret
            await ctx.author.send("Lütfen Trakt Client Secret'inizi girin:")
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_secret = msg.content.strip()

            # OAuth setup for Trakt
            redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            oauth_url = f'https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
            await ctx.author.send(f"Uygulamayı yetkilendirmek için bu URL'yi ziyaret edin: {oauth_url}\nYetkilendirme tamamlandıktan sonra lütfen yetkilendirme kodunu gönderin.")

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
                        await ctx.author.send("Trakt kimlik bilgileri başarıyla ayarlandı.")
                    else:
                        await ctx.author.send(f"Erişim tokenı alınamadı: {await response.text()}")

        except asyncio.TimeoutError:
            await ctx.author.send("Yanıt vermeniz çok uzun sürdü. Lütfen setup komutunu tekrar deneyin.")
                @trakt.command()
    async def settmdbkey(self, ctx, api_key: str):
        """TMDb API anahtarını ayarlamak veya güncellemek için komut."""
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
            await ctx.send("Trakt erişim tokenı bulunamadı. Lütfen önce kimlik bilgilerini `?trakt setup` komutunu kullanarak ayarlayın.")
            return

        if not self.data['tracked_users']:
            await ctx.send("Takip edilecek kullanıcı yok. Lütfen önce `?trakt user <kullanıcı adı>` komutunu kullanarak kullanıcı ekleyin.")
            return

        channel_id = self.data.get('channel_id')
        if channel_id is None:
            await ctx.send("Kanal ayarlanmadı. Lütfen `?trakt setupchannel <kanal id>` komutunu kullanarak kanal ayarlayın.")
            return

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            await ctx.send("Geçersiz kanal ID. Lütfen `?trakt setupchannel <kanal id>` komutunu kullanarak kanalı tekrar ayarlayın.")
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
                    embed.set_author(name=username, icon_url=ctx.author.avatar.url)  # Kullanıcı adını büyük başlık olarak ekle
                    await channel.send(embed=embed)

    async def create_embed_with_tmdb_info(self, title, content_type):
        """TMDb'den ek bilgi alarak bir embed oluşturun."""
        api_key = self.data.get('tmdb_api_key')
        if not api_key:
            return discord.Embed(title=title, description="TMDb API anahtarı ayarlanmadı.")

        url = f"https://api.themoviedb.org/3/search/{'movie' if content_type == 'movie' else 'tv'}?api_key={api_key}&query={title}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['results']:
                        item = data['results'][0]
                        embed = discord.Embed(
                            title=item.get('title', title) if content_type == 'movie' else item.get('name', title),
                            description=item.get('overview', 'Açıklama mevcut değil.'),
                            color=discord.Color.blue()
                        )
                        embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}")
                        embed.add_field(name="Puan", value=item.get('vote_average', 'N/A'), inline=True)
                        embed.add_field(name="Yayın Tarihi", value=item.get('release_date' if content_type == 'movie' else 'first_air_date', 'N/A'), inline=True)
                        return embed
                    else:
                        return discord.Embed(title=title, description="TMDb'de sonuç bulunamadı.")
                else:
                    return discord.Embed(title=title, description="TMDb'den ek bilgi alınamadı.")

    @trakt.command()
    async def setupchannel(self, ctx, *, channel: discord.TextChannel):
        self.data['channel_id'] = str(channel.id)
        self.save_data()
        await ctx.send(f"Kanal ID {channel.mention} olarak ayarlandı. Güncellemeler buraya gönderilecek.")

    @tasks.loop(minutes=30)
    async def check_for_updates(self):
        if not self.data['trakt_credentials'].get('access_token') or not self.data['tracked_users']:
            return

        channel_id = self.data.get('channel_id')
        if channel_id is None:
            return

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            print("Geçersiz kanal ID. Lütfen DISCORD_CHANNEL_ID'nizi kontrol edin.")
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
                    embed.set_author(name=username, icon_url=None)  # Kullanıcı adını büyük başlık olarak ekle
                    await channel.send(embed=embed)
            
