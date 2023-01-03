import discord
from redbot.core import commands, Config
from random import randint
import aiohttp
import logging

log = logging.getLogger("Doctor")  
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

BaseCog = getattr(commands, "Cog", object)


class Doctor(BaseCog):
    """Interact with people!"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=745214589)
        default_global = {
            "9": [
                "https://tenor.com/tr/view/doctor-doktor-doctor-who-ninth-doctor-christopher-eccleston-gif-21001148",
                "https://tenor.com/tr/view/doctor-dance-doctor-who-dances-gif-24783753",
                "https://tenor.com/tr/view/fantastic-doctor-who-gif-24783749",
                "https://tenor.com/tr/view/doctor-who-ah-doctor-who-ah-christopher-eccleston-chris-gif-16713033",
                "https://tenor.com/tr/view/nineth-doctor-9th-doctor-doctor-who-not-again-pff-gif-18293755",
                "https://tenor.com/tr/view/no-doctor-who-9th-christopher-eccleston-the-parting-of-the-ways-gif-26350828",
                
            ],
        
            "10": [
                "https://tenor.com/tr/view/10th-doctor-smile-gif-20188335",
                "https://tenor.com/tr/view/david-tennant-doctor-who-ten-tenth-doctor-tenth-gif-5187427",
                "https://tenor.com/tr/view/doctorwho-david-tennant-ten-allonsy-gif-5114776",
                "https://tenor.com/tr/view/david-tennent-doctor-who-10th-doctor-emotion-gif-9438311",
                "https://tenor.com/tr/view/yes-oh-no-david-tennant-doctor-who-space-man-gif-13540550",
                "https://tenor.com/tr/view/love-and-monsters-dr-who-tumblr-tenth-doctor-david-tennant-gif-21680903",
                "https://tenor.com/tr/view/television-tv-shows-tv-doctor-who-dr-who-gif-18824146",
                "https://tenor.com/view/doctor-who-david-tennant-shocked-gif-5905246",
                "https://tenor.com/tr/view/doctor-who-dr-who-david-tennant-smile-laugh-gif-3963005",
                "https://tenor.com/tr/view/david-tennant-doctor-who-smile-happy-gif-13595993",
            ],
            "11": [
                "https://tenor.com/view/thumbs-up-eleventh-doctor-doctor-who-matt-smith-smile-gif-17095333",
                "https://tenor.com/tr/view/bow-tie-whovian-doctor-who-gif-13949282",
                "https://tenor.com/tr/view/doctor-who-matt-smith-tardis-the-doctor-gif-10088246",
                "https://tenor.com/tr/view/doctor-who-doctor-who-whovian-matt-smith-gif-8187011",
                "https://tenor.com/tr/view/doctor-who-matt-smith-i-know-gif-10088122",
                "https://tenor.com/tr/view/doctor-who-dr-who-11th-doctor-matt-smith-i-regret-nothing-gif-3964998",
                "https://tenor.com/tr/view/doctorwho-mattsmith-eleven-huh-cool-gif-5139387",
                "https://tenor.com/tr/view/doctorwho-eleven-mattsmith-haha-funny-gif-5032015",
                "https://tenor.com/tr/view/doctorwho-mattsmith-eleven-you-stuttering-gif-5136329",
                
            ],
            "12": [
                "https://tenor.com/tr/view/doctor-who-peter-capaldi-gif-8187020",
                "https://tenor.com/tr/view/attack-eyebrows-serious-doctor-who-peter-capaldi-eyebrows-gif-17344691",
                "https://tenor.com/tr/view/peter-capaldi-doctor-who-love-wow-gif-11318396",
                "https://tenor.com/tr/view/12th-doctor-peter-capaldi-cheers-gif-20188246",
                "https://tenor.com/tr/view/doctorwho-doctormysterio-petercapaldi-twelve-christmas-gif-7488172",
                "https://tenor.com/tr/view/doctor-who-doctor-who-whovian-peter-capaldi-gif-8187014",
                "https://tenor.com/view/doctor-who-guitar-rock-and-roll-rock-on-peter-capaldi-gif-4664372",
                
            ],
            "13": [
                "https://tenor.com/tr/view/jodie-whittaker-hood-thirteenth-doctor-doctor-who-gif-20617866",
                "https://tenor.com/tr/view/doctor-who-thirteenth-doctor-jodie-whittaker-thirteen-the-doctor-gif-24425765",
                "https://tenor.com/tr/view/thirteenth-doctor-doctor-who-jodie-whittaker-13th-doctor-series13-gif-22465266",
                "https://tenor.com/view/jodie-whittaker-doctor-who-thirteenth-doctor-tux-suit-gif-20601711",
                "https://tenor.com/tr/view/doctor-who-thirteenth-doctor-jodie-whittaker-tux-spyfall-gif-20617784",
                "https://tenor.com/tr/view/doctor-who-thirteenth-doctor-jodie-whittaker-thirteen-the-doctor-gif-24425756",
                "https://tenor.com/tr/view/doctor-who-thirteenth-doctor-jodie-whittaker-thirteen-the-doctor-gif-24425768",
                
            ],
            "Amy": [
                "https://tenor.com/tr/view/doctor-who-dr-who-tumblr-amy-pond-karen-gillan-gif-20741252",
                "https://tenor.com/tr/view/doctor-who-dr-who-amy-pond-karen-gillan-hot-gif-20733634",
                "https://tenor.com/tr/view/doctor-who-dr-who-tumblr-the-eleventh-hour-amy-pond-gif-20741278",
                "https://tenor.com/tr/view/doctor-who-amy-pond-wink-smile-flirty-gif-5383445",
                "https://tenor.com/tr/view/doctor-who-karen-gillan-amy-pond-shocked-surprised-gif-7512369",
                "https://tenor.com/view/doctor-who-dr-who-tumblr-the-wedding-of-river-song-amy-pond-gif-20741182",
                "https://tenor.com/tr/view/doctor-who-amy-pond-amy-pond-cry-gif-5383457",
                "https://tenor.com/tr/view/doctor-who-amy-pond-not-sad-smile-walking-gif-5383460",
               
            ],
            "River": [
                "https://tenor.com/tr/view/spoilers-pandorica-river-song-doctor-who-gif-18293417",
                "https://tenor.com/tr/view/spoilers-doctor-who-river-song-gif-26449815",
                "https://tenor.com/tr/view/river-song-spoiler-doctor-who-matt-smith-gif-11515428",
                "https://tenor.com/tr/view/river-eleventh-doctor-matt-smith-gif-13942441",
                "https://tenor.com/tr/view/doctor-who-river-song-regeneration-gif-5358333",
                "https://tenor.com/tr/view/doctor-who-riversong-blowing-a-kiss-kiss-gif-6097447",
                "https://tenor.com/tr/view/doctor-who-river-song-sweetie-gif-9232072",
     
            ],
            "Rose": [
                "https://tenor.com/tr/view/doctor-who-dr-who-love-and-monsters-tenth-doctor-david-tennant-gif-20880623",
                "https://tenor.com/tr/view/rose-tyler-doctorwho-crying-sad-gif-5866588",
                "https://tenor.com/tr/view/yup-doctorwho-rose-tyler-teary-eyed-gif-5399528",
                "https://tenor.com/tr/view/billie-piper-doctor-who-rose-tyler-laughing-gif-14702302",
                "https://tenor.com/view/love-and-monsters-doctor-who-dr-who-tumblr-rose-tyler-gif-21693979",
                "https://tenor.com/tr/view/doctor-who-david-tennant-ten-rose-tyler-laughing-gif-5266254",
                "https://tenor.com/tr/view/i-love-you-doctor-who-crying-rose-tyler-love-gif-12183218",
                "https://tenor.com/tr/view/doctor-who-rose-tyler-bad-wolf-i-want-chips-gif-5403970",
              
            ],
            "Jack": [
                "https://tenor.com/tr/view/doctor-who-captain-jack-captain-harkness-captain-jack-harkness-innuendo-gif-18787308",
                "https://tenor.com/view/ladies-captain-jack-harkness-jack-harkness-john-barrowman-jack-gif-5987756",
                "https://tenor.com/tr/view/john-barrowman-face-of-boa-whovian-doctor-who-captain-jack-gif-12993528",
            ],
            "Donna": [
                "https://tenor.com/tr/view/doctor-who-dr-who-catherine-tate-donna-noble-thumbs-up-gif-5289862",
                "https://tenor.com/view/oi-oh-david-tennant-catherine-tate-doctor-who-gif-17272159",
                "https://tenor.com/tr/view/donna-noble-catherine-tate-bride-doctor-who-dr-who-gif-21957104",
                "https://tenor.com/tr/view/doctor-who-donna-laugh-wacky-gif-7895796",
                "https://tenor.com/tr/view/doctor-who-dr-who-partners-in-crime-donna-noble-catherine-tate-gif-20318700",
                "https://tenor.com/tr/view/doctorwho-david-tennant-ten-donna-onwards-gif-5013612",
               
            ],
            "Clara": [
                "https://tenor.com/tr/view/thumbs-up-approve-good-clara-oswald-doctor-who-gif-5199401",
                "https://tenor.com/tr/view/jenna-coleman-doctor-who-claraoswald-gif-18455004",
                "https://tenor.com/tr/view/jenna-coleman-clara-oswald-doctor-who-gif-18455028",
                "https://tenor.com/tr/view/clara-oswald-shocked-doctor-who-gif-5021709",
                "https://tenor.com/tr/view/jenna-coleman-clara-oswald-doctor-who-bbc-gif-18455000",
                "https://tenor.com/tr/view/see-you-eye-on-you-eye-to-eye-clara-oswald-doctor-who-gif-8835689",
            ],
         }
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def dokuz(self, ctx, *, user: discord.Member):
        """Hugs a user!"""

        author = ctx.message.author
        images = await self.config.dokuz()

        nekos = await self.fetch_nekos_life(ctx, "dokuz")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} hugs {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx, *, user: discord.Member):
        """Cuddles a user!"""

        author = ctx.message.author
        images = await self.config.cuddle()

        nekos = await self.fetch_nekos_life(ctx, "cuddle")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} cuddles {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, *, user: discord.Member):
        """Kiss a user!"""

        author = ctx.message.author
        images = await self.config.kiss()

        nekos = await self.fetch_nekos_life(ctx, "kiss")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} kisses {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, *, user: discord.Member):
        """Slaps a user!"""

        author = ctx.message.author
        images = await self.config.slap()

        nekos = await self.fetch_nekos_life(ctx, "slap")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} slaps {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, *, user: discord.Member):
        """Pats a user!"""

        author = ctx.message.author
        images = await self.config.pat()

        nekos = await self.fetch_nekos_life(ctx, "pat")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} pats {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx, *, user: discord.Member):
        """Licks a user!"""

        author = ctx.message.author
        images = await self.config.lick()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} licks {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx, *, user: discord.Member):
        """Highfives a user!"""

        author = ctx.message.author
        images = await self.config.highfive()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} highfives {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx, *, user: discord.Member):
        """Feeds a user!"""

        author = ctx.message.author
        images = await self.config.feed()

        nekos = await self.fetch_nekos_life(ctx, "feed")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} feeds {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, *, user: discord.Member):
        """Tickles a user!"""

        author = ctx.message.author
        images = await self.config.tickle()

        nekos = await self.fetch_nekos_life(ctx, "tickle")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} tickles {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx, *, user: discord.Member):
        """Pokes a user!"""

        author = ctx.message.author
        images = await self.config.poke()

        nekos = await self.fetch_nekos_life(ctx, "poke")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} pokes {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx):
        """Be smug towards someone!"""

        author = ctx.message.author
        images = await self.config.smug()

        smug = await self.fetch_nekos_life(ctx, "smug")
        images.extend(smug)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} is smug**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    async def fetch_nekos_life(self, ctx, rp_action):

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.nekos.dev/api/v3/images/sfw/gif/{rp_action}/?count=20") as resp:
                try:
                    content = await resp.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError) as ex:
                    log.debug("Pruned by exception, error below:")
                    log.debug(ex)
                    return []

        if content["data"]["status"]["code"] == 200:
            return content["data"]["response"]["urls"]
