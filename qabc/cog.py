import discord
from discord.ext import commands


class QCog(commands.Cog):
    """custom Cog class"""

    def __init__(self, bot: discord.Bot):
        self.bot = bot
