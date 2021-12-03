import discord
from discord.ext import commands


class QCog(commands.Cog):
    """custom Cog class"""

    def __init__(self, client: discord.Client):
        self.client = client
