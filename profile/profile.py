# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from redbot.core import Config

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7895645342)
        self.config.register_member(
            name=None, 
            age=None, 
            gender=None,
            city=None, 
            occupation=None, 
            favorite_tv_shows=None, 
            favorite_movies=None,
            hobbies=None,
            about=None
        )

    @commands.group()
    async def profil(self, ctx: commands.Context) -> None:
        """Profilinizi oluşturun veya başka birinin profilini görüntüleyin """
        pass

    @profil.command(name="oluştur")
    async def _oluştur(self, ctx):
        await ctx.author.send("Merhaba, profilinizi oluşturmak için birkaç soru sormak istiyoruz. Lütfen adınızı söyler misiniz?")
        name = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Yaşınız kaç?")
        age = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Cinsiyetiniz nedir?")
        gender = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Hangi şehirde yaşıyorsunuz?")
        city = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Mesleğiniz nedir?")
        occupation = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Hangi dizileri izlemeyi seversiniz?")
        favorite_tv_shows = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Hangi filmleri izlemeyi seversiniz?")
        favorite_movies = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)

        await ctx.author.send("Hangi hobileriniz var?")
        hobbies = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)

        await ctx.author.send("Kısaca kendinizden bahseder misiniz?")
        about = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)

        await self.config.member(ctx.author).name.set(name.content)
        await self.config.member(ctx.author).age.set(age.content)
        await self.config.member(ctx.author).gender.set(gender.content)
        await self.config.member(ctx.author).city.set(city.content)
        await self.config.member(ctx.author).occupation.set(occupation.content)
        await self.config.member(ctx.author).favorite_tv_shows.set(favorite_tv_shows.content)
        await self.config.member(ctx.author).favorite_movies.set(favorite_movies.content)
        await self.config.member(ctx.author).hobbies.set(hobbies.content)
        await self.config.member(ctx.author).about.set(about.content)
        
        await ctx.send("Profiliniz başarıyla oluşturuldu!")

    
    
