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
        is_owner = ctx.author.id == self.bot.appinfo.owner
        is_manager = ctx.author.id in self.bot.config.managers or not self.bot.config.managers
        return is_owner or is_manager

    @commands.command(aliases=["logout"])
    async def shutdown(self, ctx):
        """log bot out of discord"""
        await ctx.reply(f"{self.bot.user} shut down at {dt.now()}.")
        await self.bot.close()

    @commands.command()
    async def load(self, ctx, cog: str = "all"):
        """load an unloaded cog, or all cogs"""
        await self.handle_cog(ctx, self.bot.load_extension, cog)

    @commands.command(aliases=["ul"])
    async def unload(self, ctx, cog: str = "all"):
        """unload a loaded cog, or all cogs"""
        await self.handle_cog(ctx, self.bot.unload_extension, cog)

    @commands.command(aliases=["rl"])
    async def reload(self, ctx, cog: str = "all"):
        """reload a loaded cog, or all cogs"""
        await self.handle_cog(ctx, self.bot.reload_extension, cog)

    @commands.command(aliases=["dm"])
    async def message(self, ctx, user: discord.User, *, msg: str):
        """send a direct message to a user"""
        try:
            await user.send(msg)
        except discord.Forbidden as exc:
            return await ctx.reply("Could not message this user.")

        await ctx.reply(f"Sent message to **{user}**.")

    @commands.group(aliases=["set"])
    async def setconfig(self, ctx):
        """set a configuration setting to a new value"""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Set a configuration setting to a new value. Available settings are:\n" + cb(
                f"[-]: staffrole  | Set staff role.       Current: {self.bot.config.staff_role}",
                f"[-]: logchannel | Set log channel.      Current: {self.bot.config.logging_channel}",
                f"[-]: mprole     | Set media perms role. Current: {self.bot.config.media_perms_role}",
                f"[-]: muterole   | Set mute role.        Current: {self.bot.config.mute_role}",
                lang="md"
            ))

    @setconfig.command()
    async def staffrole(self, ctx, role: discord.Role):
        """set the staff role to a new role"""
        await ctx.reply(f"Updated staff role: `{self.bot.config.staff_role} -> {role.id}`")
        self.bot.config.staff_role = role.id

    @setconfig.command()
    async def mprole(self, ctx, role: discord.Role):
        """set the media perms role to a new role"""
        await ctx.reply(f"Updated media perms role: `{self.bot.config.media_perms_role} -> {role.id}`")
        self.bot.config.media_perms_role = role.id

    @setconfig.command()
    async def muterole(self, ctx, role: discord.Role):
        """set the media perms role to a new role"""
        await ctx.reply(f"Updated mute role: `{self.bot.config.mute_role} -> {role.id}`")
        self.bot.config.mute_role = role.id

    @setconfig.command()
    async def logchannel(self, ctx, channel: discord.TextChannel):
        """set the logging channel to a new channel"""
        await ctx.reply(f"Updated logging channel: `{self.bot.config.logging_channel} -> {channel.id}`")
        self.bot.config.logging_channel = channel.id

    @staticmethod
    async def handle_cog(ctx, func: Callable, cog: str = "all"):
        cog = cog.lower()

        func_name = {
            "unload_extension": "unload",
            "reload_extension": "reload",
            "load_extension": "load"
        }[func.__name__]  # get proper function name to use it like a verb

        embed = discord.Embed(color=discord.Color.blue())

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


def setup(bot: discord.Bot):
    bot.add_cog(Manager(bot))
