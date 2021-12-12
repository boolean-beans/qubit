import os
import discord

from typing import Optional
from discord.ext import commands
from qabc.cog import QCog
from qabc.exc import HierarchyError, SelfModError


class Moderation(QCog):
    """Moderation cog"""

    async def cog_check(self, ctx):
        """only staff may use this cog, and only in a server"""
        if ctx.guild is None:
            return False

        is_staff = self.bot.config.staff_role in map((lambda r: r.id), ctx.author.roles)
        return is_staff and ctx.guild is not None

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member: discord.Member, *, nick: Optional[str] = None):
        """set a target member's nickname, or clear it"""
        if member.top_role >= ctx.author.top_role:
            raise HierarchyError("You cannot modify this user's nickname.")

        embed = discord.Embed(
            description=f"Updated **{member}**'s nickname: `{member.display_name} -> {nick}`",
            color=discord.Color.blue()
        )

        await member.edit(nick=nick)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["ar"])
    async def addrole(self, ctx, member: discord.Member, *, role: discord.Role):
        """add a role to a target member"""
        if isinstance(role, int):
            role = ctx.guild.get_role(role)

        if member.top_role >= ctx.author.top_role:
            raise HierarchyError("You cannot modify this user's roles.")

        if role >= ctx.author.top_role:
            raise HierarchyError("This role is equal to or higher than your highest rank, and cannot be assigned or "
                                 "removed by you.")

        await member.add_roles(role)
        await ctx.reply(f"Added `{role.name}` to **{member}**.")

    @commands.command(aliases=["rr"])
    async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):
        """remove a role from a target member"""
        if isinstance(role, int):
            role = ctx.guild.get_role(role)

        if member.top_role >= ctx.author.top_role:
            raise HierarchyError("You cannot modify this user's roles.")

        if role >= ctx.author.top_role:
            raise HierarchyError("This role is equal to or higher than your highest rank, and cannot be assigned or "
                                 "removed by you.")

        await member.remove_roles(role)
        await ctx.reply(f"Removed `{role.name}` to **{member}**.")

    @commands.command(name="mediaperms", aliases=["mp"])
    async def assign_media_perms(self, ctx, *, member: discord.Member):
        """give a member the media perms role"""
        await self.addrole(ctx, member, role=self.bot.config.media_perms_role)

    @commands.command(name="mute", aliases=["stfu"])
    async def assign_mute(self, ctx, *, member: discord.Member):
        """mute a given member"""
        await self.addrole(ctx, member, role=self.bot.config.mute_role)

    @commands.command(name="skid")
    async def assign_skid(self, ctx, *, member: discord.Member):
        """assign the skid role to a given member"""
        await self.addrole(ctx, member, role=self.bot.config.skid_role)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason: str = "No reason given"):
        """ban a target member, by ID or mention"""
        if user := discord.utils.get(ctx.guild.members, id=user.id):
            if user.id == ctx.author.id:
                raise SelfModError("You cannot ban yourself.")

            if user.top_role >= ctx.author.top_role:
                raise HierarchyError("You cannot ban this member.")

        await ctx.guild.ban(discord.Object(id=user.id))

        embed = discord.Embed(title="Reason:", description=reason, color=discord.Color.red())

        embed.set_author(name=f"{user} banned", icon_url=user.avatar.url)
        embed.set_footer(text=f"Banned by {ctx.author}\nUID: {user.id}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason given"):
        """kick a target member, by ID or mention"""
        if member.id == ctx.author.id:
            raise SelfModError("You cannot kick yourself.")

        if member.top_role >= ctx.author.top_role:
            raise HierarchyError("You cannot kick this member.")

        await member.kick(reason=reason)

        embed = discord.Embed(title="Reason:", description=reason, color=discord.Color.random(seed=member.id))
        embed.set_author(name=f"{member} kicked", icon_url=member.avatar.url)
        embed.set_footer(text=f"Kicked by {ctx.author}\nUID: {member.id}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        """revoke ban from a banned user"""
        try:
            await ctx.guild.unban(user)
        except discord.HTTPException:
            raise Exception("This user has not been banned.")

        await ctx.reply(f"Unbanned `{user} ({user.id})`.")


def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))
