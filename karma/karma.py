import discord
from redbot.core import commands
import random
import asyncio
from redbot.core.data_manager import bundled_data_path

class Karma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wordlist_file = str(bundled_data_path(self) / 'data.txt')
        self.active_games = {}  # Oyunu başlatan kişiyi takip etmek için bir sözlük
        self.points = {}  # Oyuncuların puanlarını saklamak için bir sözlük

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
            return msg.channel == ctx.channel

        try:
            start_time = asyncio.get_event_loop().time()
            while True:
                # Kullanıcının cevabını bekleyin
                msg = await self.bot.wait_for('message', check=check, timeout=20.0)
                end_time = asyncio.get_event_loop().time()
                elapsed_time = int(end_time - start_time)
                if msg.content.lower() == word.lower():
                    points_earned = 20 - elapsed_time
                    if points_earned < 1:
                        points_earned = 1
                    await ctx.send(f"Doğru! Kelime: `{word}`. {points_earned} puan kazandınız.")
                    self.points[msg.author.id] = self.points.get(msg.author.id, 0) + points_earned
                    break  # Oyunu bitir
                else:
                    await ctx.send("Yanlış! Bir dahaki sefere daha iyi şanslar.")

            # Oyunu başlatan kişiyi kaydet
            self.active_games[ctx.author.id] = True
        except asyncio.TimeoutError:
            await ctx.send("Süre doldu! Zamanında cevap vermediniz.")

    @commands.command()
    async def puanlar(self, ctx):
        if self.points:
            message = "Puanlar:\n"
            for user_id, points in self.points.items():
                user = ctx.guild.get_member(user_id)
                if user:
                    message += f"{user.name}: {points} puan\n"
            await ctx.send(message)
        else:
            await ctx.send("Henüz kimse puan almamış.")

    @commands.command()
    async def puan_sifirla(self, ctx):
        if ctx.author.id in self.points:
            self.points[] = 0
            await ctx.send(f"{ctx.author.name} puanları sıfırlandı.")
        else:
            await ctx.send(f"{ctx.author.name} zaten 0 puana sahip.")

def setup(bot):
    bot.add_cog(Corba(bot))
