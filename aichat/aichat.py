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
        self.device: str = "cpu"
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
            
            self.to
