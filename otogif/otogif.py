import discord
from redbot.core import commands, Config
import random

class Otogif(commands.Cog):
    def __init__(self, bot):      
        self.bot = bot
        self.config = Config.get_conf(self, identifier=145256632)
        self.config.register_guild(gifs=[])

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author == self.bot.user:
         return

      gifs = await self.config.guild(message.guild).gifs()
      matching_gifs = [gif for gif in gifs if gif["trigger"] == message.content]
      if matching_gifs:
        gif = random.choice(matching_gifs)
        embed = discord.Embed()
        embed.set_image(url=gif["gif_url"])
        await message.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addgif(self, ctx, gif_url: str, trigger: str):
     gifs = await self.config.guild(ctx.guild).gifs()
     gifs.append({"trigger": trigger, "gif_url": gif_url})
     await self.config.guild(ctx.guild).gifs.set(gifs)
     await ctx.send(f'Added trigger "{trigger}" with gif URL "{gif_url}"')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def listgifs(self, ctx):
        gifs = await self.config.guild(ctx.guild).gifs()
        if not gifs:
           await ctx.send('No triggers found')
        else:
           message = 'Triggers:\n'
           for gif in gifs:
               message += f'- {gif["trigger"]}\n'
           await ctx.send(message)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removegif(self, ctx, *triggers: str):
        gifs = await self.config.guild(ctx.guild).gifs()
        gifs = [gif for gif in gifs if gif["trigger"] not in triggers]
        await self.config.guild(ctx.guild).gifs.set(gifs)
        trigger_str = ', '.join(triggers)
