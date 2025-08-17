import asyncio
import aiohttp
import logging
import os
import zipfile
from pathlib import Path
from typing import Optional

import discord
import torch
from redbot.core import commands, Config, data_manager
from redbot.core.utils.chat_formatting import box, humanize_list

try:
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

log = logging.getLogger("red.aichat")


class AIChat(commands.Cog):
    """AI chatbot using fine-tuned GPT-2 model"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)

        default_global = {
            "model_url": None,
            "model_loaded": False,
            "max_length": 50,
            "temperature": 0.7,
            "response_chance": 0.05,
        }

        default_guild = {
            "enabled_channels": [],
            "prefix_responses": True,
            "max_response_length": 200,
        }

        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

        self.model: Optional[GPT2LMHeadModel] = None
        self.tokenizer: Optional[GPT2Tokenizer] = None
        self.model_path: Path = data_manager.cog_data_path(self) / "model"
        self.model_path.mkdir(exist_ok=True)

        if TRANSFORMERS_AVAILABLE:
            asyncio.create_task(self._load_model_if_exists())

    def cog_unload(self):
        if self.model:
            del self.model
        if self.tokenizer:
            del self.tokenizer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    async def _load_model_if_exists(self):
        if (self.model_path / "config.json").exists():
            await self._load_model()
        else:
            log.info("No model found. Use `aichat setup` to download a model.")

    async def _load_model(self):
        try:
            log.info("Loading AI model...")
            self.tokenizer = GPT2Tokenizer.from_pretrained(str(self.model_path))
            self.model = GPT2LMHeadModel.from_pretrained(
                str(self.model_path),
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True
            )
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(device)
            self.model.eval()
            await self.config.model_loaded.set(True)
            log.info(f"AI model loaded successfully on {device}")
        except Exception as e:
            log.error(f"Failed to load model: {e}")
            await self.config.model_loaded.set(False)

    async def _generate_response(self, prompt: str) -> Optional[str]:
        if not self.model or not self.tokenizer:
            return None
        try:
            max_length = await self.config.max_length()
            temperature = await self.config.temperature()

            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=100)
            if torch.cuda.is_available():
                inputs = inputs.cuda()

            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2,
                    early_stopping=True
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if response.startswith(prompt):
                response = response[len(prompt):].strip()

            return response if response and len(response) > 3 else None
        except Exception as e:
            log.error(f"Error generating response: {e}")
            return None

    @commands.group(name="aichat")
    async def aichat(self, ctx):
        """AI Chat configuration commands"""
        pass

    @aichat.command(name="setup")
    @commands.is_owner()
    async def setup_model(self, ctx, model_url: str = None):
        if not TRANSFORMERS_AVAILABLE:
            await ctx.send("❌ Transformers library not installed. Please install requirements.")
            return
        if not model_url:
            await ctx.send("Please provide a URL to download the model from.")
            return

        await ctx.send("📥 Downloading model... This may take a few minutes.")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(model_url) as resp:
                    if resp.status != 200:
                        await ctx.send(f"❌ Failed to download model: HTTP {resp.status}")
                        return
                    temp_file = self.model_path / "model.zip"
                    with open(temp_file, "wb") as f:
                        async for chunk in resp.content.iter_chunked(8192):
                            f.write(chunk)

            await ctx.send("📦 Extracting model files...")
            with zipfile.ZipFile(temp_file, "r") as zip_ref:
                zip_ref.extractall(self.model_path)
            temp_file.unlink()

            await ctx.send("🔄 Loading model...")
            await self._load_model()

            if await self.config.model_loaded():
                await ctx.send("✅ Model setup complete! AI chat is now available.")
            else:
                await ctx.send("❌ Model setup failed. Check logs for details.")

        except Exception as e:
            await ctx.send(f"❌ Setup failed: {str(e)}")
            log.error(f"Model setup error: {e}")

    @aichat.command(name="status")
    async def status(self, ctx):
        model_loaded = await self.config.model_loaded()
        if model_loaded and self.model:
            device = next(self.model.parameters()).device
            embed = discord.Embed(title="AI Chat Status", color=0x00ff00)
            embed.add_field(name="Status", value="✅ Loaded", inline=True)
            embed.add_field(name="Device", value=str(device), inline=True)
            embed.add_field(name="Model Path", value=str(self.model_path), inline=False)
        else:
            embed = discord.Embed(title="AI Chat Status", color=0xff0000)
            embed.add_field(name="Status", value="❌ Not loaded", inline=True)
            embed.add_field(name="Setup Required", value="Use `aichat setup <url>`", inline=False)
        await ctx.send(embed=embed)

    @aichat.command(name="channel")
    @commands.admin_or_permissions(manage_channels=True)
    async def toggle_channel(self, ctx, channel: discord.TextChannel = None):
        if not await self.config.model_loaded():
            await ctx.send("❌ AI model not loaded. Use `aichat setup` first.")
            return
        channel = channel or ctx.channel
        enabled_channels = await self.config.guild(ctx.guild).enabled_channels()
        if channel.id in enabled_channels:
            enabled_channels.remove(channel.id)
            await self.config.guild(ctx.guild).enabled_channels.set(enabled_channels)
            await ctx.send(f"🔇 AI disabled in {channel.mention}")
        else:
            enabled_channels.append(channel.id)
            await self.config.guild(ctx.guild).enabled_channels.set(enabled_channels)
            await ctx.send(f"🔊 AI enabled in {channel.mention}")

    @commands.command(name="chat")
    async def chat_command(self, ctx, *, message: str):
        if not await self.config.model_loaded():
            await ctx.send("❌ AI model not loaded.")
            return
        async with ctx.typing():
            response = await self._generate_response(message)
        if response:
            max_len = await self.config.guild(ctx.guild).max_response_length()
            if len(response) > max_len:
                response = response[: max_len - 3] + "..."
            await ctx.reply(response)
        else:
            await ctx.send("🤔 I couldn't generate a response to that.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        if not await self.config.model_loaded():
            return
        enabled_channels = await self.config.guild(message.guild).enabled_channels()
        if message.channel.id not in enabled_channels:
            return

        bot_mentioned = self.bot.user in message.mentions
        import random
        response_chance = await self.config.response_chance()
        should_respond_randomly = random.random() < response_chance

        if bot_mentioned or should_respond_randomly:
            async with message.channel.typing():
                response = await self._generate_response(message.content)
            if response:
                max_len = await self.config.guild(message.guild).max_response_length()
                if len(response) > max_len:
                    response = response[: max_len - 3] + "..."
                prefix_response = await self.config.guild(message.guild).prefix_responses()
                if prefix_response and not bot_mentioned:
                    await message.reply(response)
                else:
                    await message.channel.send(response)


def setup(bot):
    if not TRANSFORMERS_AVAILABLE:
        raise RuntimeError(
            "The transformers library is required for this cog. Install it with `pip install transformers torch`"
        )
   
