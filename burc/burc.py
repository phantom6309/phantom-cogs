# Post animal pics by Eslyium#1949 & Yukirin#0048

# Discord
import discord
import requests
import json
from googletrans import Translator
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
    async def akrep(self, ctx,):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "scorpio", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        ch = 'text='
        r2=r.split(ch, 1)[1]
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Akrep"} \n {r3}.')
        
       

    @commands.command()
    
    async def başak(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "virgo", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Başak"} \n {r3}.')
   
    @commands.command()
    async def koç(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "aries", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Koç"} \n {r3}.')

    @commands.command()
    async def aslan(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "leo", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Aslan"} \n {r3}.')
    @commands.command()
    
    async def yay(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "sagittarius", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Yay"} \n {r3}.')

    
    @commands.command()
    
    async def boğa(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "taurus", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Boğa"} \n {r3}.')
        

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def oğlak(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "capricorn", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Oğlak"} \n {r3}.')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def ikizler(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "gemini", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"İkizler"} \n {r3}.')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def terazi(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "libra", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        ch = 'text='
        r2=r.split(ch, 1)[1]
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Terazi"} \n {r3}.')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def kova(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "aquarius", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Kova"} \n {r3}.')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def yengeç(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "cancer", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Yengeç"} \n {r3}.')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def balık(self, ctx):
        """Shows a cat"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": "pisces", "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest='tr'))
        r2=r.strip('Translated(src=en, dest=tr, text=')
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        await ctx.send(f'{"Balık"} \n {r3}.')

    @commands.command()
    
    async def kur(self, ctx):
        """Shows a cat"""
        endpoint = "https://api.genelpara.com/embed/doviz.json"
        
        response = requests.post(endpoint)
        embed = discord.Embed(title="Kur")

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
    
    async def eczane(self, ctx, ilce: str, il: str):
           url = "https://api.collectapi.com/health/dutyPharmacy"
           headers = {'authorization':'apikey 30d5SeFaSenqEvTFHaJjXI:71pwcsZRZA2qxRi2vNJVmX','content-type':'application/json',}
           params = {'ilce': ilce,'il': il,}
           response = requests.get(url, headers=headers, params=params)
           data = response.json()
           embed = discord.Embed(title="Nöbetçi")
           Isim = data['result'][0]['name']
           Telefon = data['result'][0]['phone']
           Adres = data['result'][0]['address']
           Isim2 = data['result'][1]['name']
           Telefon2 = data['result'][1]['phone']
           Adres2 = data['result'][1]['address']
           #Isim3 = data['result'][2]['name']
           #Telefon3 = data['result'][2]['phone']
           #Adres3 = data['result'][2]['address']
           embed.add_field(name="isim", value=Isim)
           embed.add_field(name="telefon", value=Telefon)
           embed.add_field(name="address", value=Adres)
           embed.add_field(name="isim", value=Isim2)
           embed.add_field(name="telefon", value=Telefon2)
           embed.add_field(name="address", value=Adres2)
           #embed.add_field(name="isim", value=Isim3)
           #embed.add_field(name="telefon", value=Telefon3)
           #embed.add_field(name="address", value=Adres3)
           await ctx.send(embed=embed)

    @commands.command()
    async def tdk(ctx, word: str):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        URL = f"https://sozluk.gov.tr/gts?ara={word}"
        response = requests.get(URL, headers=headers)
        data = response.json()
        meanings = []
        embed = discord.Embed(title="tdk")
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)
        
    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    __del__ = cog_unload
