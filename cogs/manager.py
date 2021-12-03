import os
import discord

from typing import Callable
from datetime import datetime as dt
from discord.ext import commands
from qabc.cog import QCog
from utils import codeblock as cb


class Manager(QCog):
    """Manager cog"""

    async def cog_check(self, ctx):
        """only bot managers may use this cog"""
        is_owner = ctx.author.id == self.client.appinfo.owner
        is_manager = ctx.author.id in self.client.config.managers or not self.client.config.managers
        return is_owner or is_manager

    @commands.command(aliases=["logout"])
    async def shutdown(self, ctx):
        """log client out of discord"""
        await ctx.reply(f"{self.client.user} shut down at {dt.now()}.")
        await self.client.close()

    @commands.command()
    async def load(self, ctx, cog: str = "all"):
        """load an unloaded cog, or all cogs"""
        await self.handle_cog(ctx, self.client.load_extension, cog)

    @commands.command(aliases=["ul"])
    async def unload(self, ctx, cog: str = "all"):
        """unload a loaded cog, or all cogs"""
        await self.handle_cog(ctx, self.client.unload_extension, cog)

    @commands.command(aliases=["rl"])
    async def reload(self, ctx, cog: str = "all"):
        """reload a loaded cog, or all cogs"""
        await self.handle_cog(ctx, self.client.reload_extension, cog)

    @commands.command(aliases=["dm"])
    async def message(self, ctx, user: discord.User, *, msg: str):
        """send a direct message to a user"""
        try:
            await user.send(msg)
        except discord.Forbidden as exc:
            return await ctx.reply("Could not message this user.")

        await ctx.reply(f"Sent message to **{user}**.")

    async def handle_cog(self, ctx, func: Callable, cog: str = "all"):
        cog = cog.lower()

        func_name = {
            "unload_extension": "unload",
            "reload_extension": "reload",
            "load_extension": "load"
        }[func.__name__]  # get proper function name to use it like a verb

        embed = discord.Embed(
            color = discord.Color.blue()
        )

        if cog == "all":
            message = []
            for i, file in enumerate(os.listdir("./cogs")):
                if file.endswith(".py"):
                    cog = file[:-3]
                    try:
                        func(f"cogs.{cog}")
                        message.append(f"+ [{i}] cog \"{cog}\" {func_name}ed successfully\n")
                    except Exception as e:
                        message.append(f"- [{i}] unable to {func_name} cog \"{cog}\". {e.__class__.__name__}: {e}\n")

            embed.description = cb(*message, lang="diff")
            return await ctx.reply(embed=embed)

        try:
            func(f"cogs.{cog}")
            embed.description = cb(f"+ cog \"{cog}\" {func_name}ed successfully", lang="diff")
        except Exception as e:
            embed.description = cb(
                f"- unable to {func_name} cog \"{cog}\". {e.__class__.__name__}: {e}"
            )

        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def foo(self, ctx):
        await ctx.reply("bar")


def setup(client: discord.Client):
    client.add_cog(Manager(client))
