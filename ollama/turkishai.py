import discord
import aiosqlite
import aiohttp
from redbot.core import commands

class TurkishAI(commands.Cog):
    """Turkish AI with message memory using Ollama."""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "/data/messages.db"  # Adjust if needed
        self.ollama_url = "http://ollama:11434/api/generate"
        self.bot.loop.create_task(self._init_db())

    async def _init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author TEXT,
                    content TEXT,
                    channel_id TEXT,
                    timestamp TEXT
                )
            """)
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO messages (author, content, channel_id, timestamp) VALUES (?, ?, ?, ?)",
                (message.author.name, message.content, str(message.channel.id), str(message.created_at))
            )
            await db.commit()

    @commands.command()
    async def askai(self, ctx, *, question: str):
        """Ask something based on message history."""
        await ctx.trigger_typing()

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT author, content FROM messages WHERE channel_id = ? ORDER BY id DESC LIMIT 10",
                (str(ctx.channel.id),)
            )
            rows = await cursor.fetchall()

        history = "\n".join(reversed([f"{a}: {c}" for a, c in rows]))

        prompt = (
            f"Aşağıda Discord kanalında geçen son konuşmalar yer almakta.\n"
            f"Bunlara dayanarak {ctx.author.name} adlı kullanıcının sorusuna cevap ver:\n\n"
            f"{history}\n\n"
            f"{ctx.author.name}: {question}\n\nAI:"
        )

        payload = {
            "model": "mixtral",
            "prompt": prompt,
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.ollama_url, json=payload) as resp:
                data = await resp.json()
                reply = data.get("response", "Cevap alınamadı.")

        await ctx.send(reply[:2000])  # Discord message length limit
