

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
    """"""

    def __init__(self, bot):
        self.bot = bot
  

    




    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    async def astro(self, ctx, sign: str, lang: str):
        """Günlük burç yorumunuzu gösterir"""
        endpoint = "https://aztro.sameerkumar.website/"
        params = { "sign": sign, "day": "today"}
        response = requests.post(endpoint, params=params)
        data = response.json()
        translator = Translator()
        r = data['description']
        r = str(translator.translate(r, dest=lang))
        ch = 'text='
        r2=r.split(ch, 1)[1]
        ch = '.,'
        r3=r2.split(ch, 1)[0]
        sign = str(translator.translate(sign, dest=lang))
        await ctx.send(f'{sign} \n {r3}.')
        
       

    

    @commands.command()
    async def kur(self, ctx):
        """Güncel döviz kurunu gösterir"""
        endpoint = "https://api.genelpara.com/embed/doviz.json"
        
        response = requests.post(endpoint)
        embed = discord.Embed(title="Kur")

        # Add the values from the response to the embed
        for key, value in response.json().items():
         embed.add_field(name=key, value=value)

        # Send the embed to the channel
        await ctx.send(embed=embed)


    
   
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
    async def tdk(self, ctx, word):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://sozluk.gov.tr/gts?ara={word}"
        response = requests.get(url, headers=headers)
        data = response.json()

        definitions = []
        for definition_data in data[0]["anlamlarListe"]:
            definition = definition_data["anlam"]
            definitions.append(definition)

        if not definitions:
            await ctx.send(f"No definitions found for {word}.")
            return   

        message = f"{word} kelimesinin anlamları:\n"
        for i, definition in enumerate(definitions):
            message += f"{i+1}. {definition}\n"
        await ctx.send(message)
       


    
