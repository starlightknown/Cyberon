import os
import sys

import discord
import yaml
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', pass_ctx=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *args):
        """
        Kick a user out of the server.
        """
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=config["error"]
            )
            await ctx.send(embed=embed)
        else:
            try:
                reason = " ".join(args)
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{ctx.message.author}**!",
                    color=config["success"]
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await ctx.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{ctx.message.author}**!\nReason: {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user.",
                    color=config["success"]
                )
                await ctx.message.channel.send(embed=embed)

    @commands.command(name="nick")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, name: str):
        """
        Change the nickname of a user on a server.
        """
        try:
            if name.lower() == "!reset":
                name = None
            await member.change_nickname(name)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{name}**!",
                color=config["success"]
            )
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user.",
                color=config["success"]
            )
            await ctx.message.channel.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *args):
        """
        Bans a user from the server.
        """
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=config["success"]
                )
                await ctx.send(embed=embed)
            else:
                reason = " ".join(args)
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{ctx.message.author}**!",
                    color=config["success"]
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await ctx.send(embed=embed)
                await member.send(f"You were banned by **{ctx.message.author}**!\nReason: {reason}")
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user.",
                color=config["success"]
            )
            await ctx.send(embed=embed)

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *args):
        """
        Warns a user in his private messages.
        """
        reason = " ".join(args)
        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{ctx.message.author}**!",
            color=config["success"]
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await ctx.send(embed=embed)
        try:
            await member.send(f"You were warned by **{ctx.message.author}**!\nReason: {reason}")
        except:
            pass

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def purge(self, ctx, number):
        """
        Delete a number of messages.
        """
        try:
            number = int(number)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"`{number}` is not a valid number.",
                color=config["error"]
            )
            await ctx.send(embed=embed)
            return
        if number < 1:
            embed = discord.Embed(
                title="Error!",
                description=f"`{number}` is not a valid number.",
                color=config["error"]
            )
            await ctx.send(embed=embed)
            return
        purged_messages = await ctx.message.channel.purge(limit=number)
        embed = discord.Embed(
            title="Chat Cleared!",
            description=f"**{ctx.message.author}** cleared **{len(purged_messages)}** messages!",
            color=config["success"]
        )
        await ctx.send(embed=embed)

    @commands.command(name='addrole')
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def setrank(self, ctx, member: discord.Member=None, *rankName: str):
        '''sets role
        -----------
        cyb!setrole <@Discord ID> Member
        '''
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.add_roles(rank)
            await ctx.send(f':white_check_mark: Role **{rank.name}** has been added for **{member.name}**')
        else:
            await ctx.send(':no_entry: you must be an admin!')

    @commands.command(pass_context=True, name='rmrole')
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def rmrank(self, ctx, member: discord.Member=None, *rankName: str):
        '''
        removes role
        -----------
        cyb!rmrole <@Discord ID> Member
        '''
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.remove_roles(rank)
            await ctx.send(f':white_check_mark: Role **{rank.name}** has been removed for **{member.name}**')
        else:
            await ctx.send(':no_entry: You must be an admin!')



def setup(bot):
    bot.add_cog(moderation(bot))
