import os
import discord

from datetime import datetime as dt
from typing import List
from discord.ext import commands
from qabc.config import Config


class Qubit(commands.Bot):
    """custom Bot class"""

    def __init__(self, *args, load_jsk: bool = True, **kwargs):
        """initialze bot object"""
        super().__init__(*args, **kwargs)
        self.command_prefix = commands.when_mentioned_or(*self.prefixes)
        self.load_jsk = load_jsk
        self.config = Config()
        self.load_extensions()

    @property
    def prefixes(self) -> List[str]:
        """bot command prefix[es]"""
        return ["q."]

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

        if not hasattr(self, "appinfo"):
            self.appinfo = await self.application_info()
