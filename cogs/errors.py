import discord

from datetime import datetime as dt
from discord.ext import commands
from qabc.exc import QubitBaseException
from qabc.cog import QCog
from utils import codeblock as cb


class Errors(QCog):
    """Errors cog"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cd_cache = {}

    @QCog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, (
            commands.CommandNotFound, commands.NotOwner,
            discord.ConnectionClosed, commands.CheckFailure,
        )):
            return  # these errors are ignorable

        cause = error.__cause__ or error
        embed = discord.Embed(color=discord.Color.red())
        del_after = None

        if isinstance(cause, (discord.Forbidden, commands.BotMissingPermissions)):
            embed.description = "I do not have permission to do that."

        elif isinstance(cause, QubitBaseException):
            embed.description = f"**{cause.__class__.__name__}**: {cause}"

        elif isinstance(cause, commands.CommandOnCooldown):
            if not self.respond_check(ctx.author.id):
                return
            del_after = 5
            embed.description = f"You are on cooldown. Try again in __**{cause.retry_after:.2f}**__ seconds."
        else:
            embed.title = "Unhandled exception"
            embed.description = cb(f"- {cause.__class__.__name__} ({error.__class__.__name__}): {error}", lang="diff")

        await ctx.reply(embed=embed, delete_after=del_after)

    def respond_check(self, uid: int) -> bool:
        """return whether or not to respond to a cooldown error,
           so as to prevent spamming, and therefore no rate limits"""

        if uid in self.cd_cache:
            delta = dt.now() - self.cd_cache[uid]
            if delta.seconds < self.client.config.cd_rate:
                return False

        self.cd_cache[uid] = dt.now()

        if len(self.cd_cache) > 50:  # if more than 50 entries exist, delete old ones
            to_delete = []
            for key, value in self.cd_cache.items():
                delta = dt.now() - value
                if delta.seconds > self.client.config.cd_rate:
                    to_delete.append(key)

            for key in to_delete:
                del self.cd_cache[key]

        return True


def setup(client):
    client.add_cog(Errors(client))