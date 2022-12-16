# Post animal pics by Eslyium#1949 & Yukirin#0048

# Discord
import discord
import requests
# Red
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, humanize_list
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

# Libs
import aiohttp

BaseCog = getattr(commands, "Cog", object)
class Burc(BaseCog):
    """Animal commands."""

    def __init__(self, bot):
        self.bot = bot
  

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def burc(self, ctx,):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "scorpio", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Akrep")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)
       

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def başak(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "virgo", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Başak")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def koç(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "aries", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Koç")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def aslan(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "leo", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Aslan")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def yay(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "sagittarius", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Yay")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def boğa(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "taurus", "day": "today"}
        response = requests.post(endpoint, params=params)
        
        embed = discord.Embed(title="Boğa")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def oğlak(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "capricorn", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Oğlak")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def ikizler(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "gemini", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="İkizler")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def terazi(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "libra", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Terazi")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def kova(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "aquarius", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Kova")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def yengeç(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "cancer", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Yengeç")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def balık(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "pisces", "day": "today"}
        response = requests.post(endpoint, params=params)
        embed = discord.Embed(title="Balık")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def kur(self, ctx):
        """Shows a cat"""
        endpoint = "https://api.genelpara.com/embed/doviz.json"
        
        response = requests.post(endpoint)
        embed = discord.Embed(title="Balık")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)


    @commands.command()
    async def havadurumu(self, ctx, *, location):
        # Send a request to the OpenWeatherMap API to get the current weather
        # for the specified location
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid=a065235d36f27c780a5ac9f345c28194')
        weather_data = r.json()

        # Extract the relevant information from the API response
        city = weather_data['name']
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        temperature = temperature - 272
        description = weather_data['weather'][0]['description']

        # Send a message to the discord channel with the weather information
        await ctx.send(f'The weather in {city}, {country} is currently {temperature} degrees and {description}.')
   
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def eczane(self, ctx, ilce: str, il: str):
           url = "https://api.collectapi.com/health/dutyPharmacy"
           headers = {'authorization':'apikey 30d5SeFaSenqEvTFHaJjXI:71pwcsZRZA2qxRi2vNJVmX','content-type':'application/json',}
           params = {'ilce': ilce,'il': il,}
           r = requests.get(url, headers=headers, params=params)
           veri = r.json()
           isim = veri['name']
           adres = veri['address']
           telefon = veri['phone']
           embed = discord.Embed(title="nobetçi")
           embed.add_field(title = "isim", description='isim')
           embed.add_field(title = "adres", description='adres')
           embed.add_field(title = "telefon", description='telefon')
           await ctx.send(embed=embed)
    
    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    __del__ = cog_unload
