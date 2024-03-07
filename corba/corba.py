import discord
from redbot.core import commands
import random
import asyncio
from redbot.core.data_manager import bundled_data_path

class Corba(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wordlist_file = str(bundled_data_path(self) / 'data.txt')
        self.points = {}

    @commands.command()
    async def karma(self, ctx):
        # Word listesini dosyadan yükle
        with open(self.wordlist_file, 'r') as f:
            words = f.readlines()
        # Listeden rastgele bir kelime seç
        word = random.choice(words).strip()
        scrambled_word = ''.join(random.sample(word, len(word)))

        await ctx.send(f"Bu kelimeyi çözün: `{scrambled_word}`")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            while True:
                # Kullanıcının cevabını bekleyin
                msg = await self.bot.wait_for('message', check=check, timeout=20.0)
                if msg.content.lower() == word.lower():
                    await ctx.send(f"Doğru! Kelime: `{word}`.")
                    self.points[ctx.author.id] = self.points.get(ctx.author.id, 0) + 1
                    break  # Oyunu bitir
                else:
                    await ctx.send("Yanlış! Bir dahaki sefere daha iyi şanslar.")
        except asyncio.TimeoutError:
            await ctx.send("Süre doldu! Zamanında cevap vermediniz.")

    @commands.command()
    async def puanlar(self, ctx):
        if ctx.author.id in self.points:
            await ctx.send(f"{ctx.author.name} {self.points[ctx.author.id]} puanına sahip.")
        else:
            await ctx.send(f"{ctx.author.name} 0 puana sahip.")


