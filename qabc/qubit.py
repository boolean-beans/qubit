import os
from abc import ABC

import discord

from datetime import datetime as dt
from typing import List, Optional
from discord.ext import commands
from qabc.config import Config


class Qubit(commands.Bot, ABC):
    """custom Bot class"""

    def __init__(self, *args, load_jsk: bool = True, **kwargs):
        """initialize bot object"""
        super().__init__(*args, **kwargs)
        self.command_prefix = commands.when_mentioned_or(*self.prefixes)
        self.load_jsk = load_jsk
        self.config = Config()
        self.appinfo = None
        self.load_extensions()

    def load_extensions(self):
        """load all available cogs"""
        if self.load_jsk:
            self.load_extension("jishaku")
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                self.load_extension(f"cogs.{file[:-3]}")

    async def on_ready(self):
        """on activation of the bot, this is called"""
        print(f"{self.user.name} brought online at {dt.now()}.")
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"boolean beans. @ me for help.")
        await self.change_presence(status=discord.Status.dnd, activity=activity)

        if self.appinfo is None:
            self.appinfo = await self.application_info()

    @property
    def logging_channel(self) -> Optional[discord.TextChannel]:
        return self.get_channel(self.config.logging_channel)

    @property
    def prefixes(self) -> List[str]:
        """bot command prefix[es]"""
        return ["q."]
