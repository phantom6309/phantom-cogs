# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
import sqlite3
import random

class Otogif(commands.Cog):
    def __init__(self, bot, db_conn):      
        self.bot = bot
        self.conn = db_conn       
    def init_db(self):

        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS trigger_gif_pairs
                     (trigger text, gif_url text)''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author == self.bot.user:
         return

      c = self.conn.cursor()
      c.execute('''SELECT gif_url FROM trigger_gif_pairs WHERE trigger=?''',
              (message.content,))
      gif_urls = c.fetchall()
      if gif_urls:
        gif_url = random.choice(gif_urls)[0]  # Select a random gif URL from the list
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addgif(self, ctx, trigger: str, gif_url: str):
     c = self.conn.cursor()
     c.execute('''INSERT INTO trigger_gif_pairs (trigger, gif_url)
                 VALUES (?, ?)''', (trigger, gif_url))
     self.conn.commit()
     await ctx.send(f'Added trigger "{trigger}" with gif URL "{gif_url}"')


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def listgifs(self, ctx):
        c = self.conn.cursor()
        c.execute('''SELECT trigger FROM trigger_gif_pairs''')
        triggers = c.fetchall()
        if not triggers:
           await ctx.send('No triggers found')
        else:
           message = 'Triggers:\n'
           for trigger, in triggers:
               message += f'- {trigger}\n'
           await ctx.send(message)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removegif(self, ctx, *triggers: str):
        c = self.conn.cursor()
        for trigger in triggers:
            c.execute('''DELETE FROM trigger_gif_pairs WHERE trigger=?''', (trigger,))
        self.conn.commit()
        trigger_str = ', '.join(triggers)
        await ctx.send(f'Removed triggers "{trigger_str}"')


