import discord
from redbot.core import commands
import random
import asyncio

class Corba(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wordlist_file = 'data.txt'
        self.points = {}

    @commands.command()
    async def unscramble(self, ctx):
        # Load word list from file
        with open(self.wordlist_file, 'r') as f:
            words = f.readlines()
        # Select a random word from the list
        word = random.choice(words).strip()
        scrambled_word = ''.join(random.sample(word, len(word)))

        await ctx.send(f"Unscramble this word: `{scrambled_word}`")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            # Wait for the player's response
            msg = await self.bot.wait_for('message', check=check, timeout=20.0)
            if msg.content.lower() == word.lower():
                await ctx.send(f"Correct! The word was `{word}`.")
                self.points[ctx.author.id] = self.points.get(ctx.author.id, 0) + 1
            else:
                await ctx.send("Incorrect! Better luck next time.")
        except asyncio.TimeoutError:
            await ctx.send("Time's up! You didn't answer in time.")

    @commands.command()
    async def points(self, ctx):
        if ctx.author.id in self.points:
            await ctx.send(f"{ctx.author.name} has {self.points[ctx.author.id]} points.")
        else:
            await ctx.send(f"{ctx.author.name} has 0 points.")

def setup(bot):
    bot.add_cog(WordUnscramble(bot))
