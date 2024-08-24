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
        elif 'show' in activity_item:
            return activity_item['show']['title'], 'tv'
        return 'Bilinmeyen Başlık', 'unknown'

    @commands.group(name='trakt', invoke_without_command=True)
    async def trakt(self, ctx):
        await ctx.send("Mevcut komutlar: `user`, `setup`, `run`, `setupchannel`, `settmdbkey`")

    @trakt.command()
    async def setup(self, ctx):
        await ctx.author.send("Lütfen Trakt Client ID'nizi sağlayın:")
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        try:
            # Trakt Client ID'yi alın
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_id = msg.content.strip()

            # Trakt Client Secret'ı alın
            await ctx.author.send("Lütfen Trakt Client Secret'ınızı sağlayın:")
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            client_secret = msg.content.strip()

            # Trakt OAuth kurulumu
            redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            oauth_url = f'https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
            await ctx.author.send(f"Lütfen bu URL'yi ziyaret ederek uygulamayı yetkilendirin: {oauth_url}\nYetkilendirmeden sonra yetkilendirme kodunu bana gönderin.")

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
                        await ctx.author.send(f"Erişim tokenı alınamadı: {await response.text()}")

        except asyncio.TimeoutError:
            await ctx.author.send("Yanıt vermeniz çok uzun sürdü. Lütfen setup komutunu tekrar deneyin.")
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
        
