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


class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    async def shutdown(self, ctx):
        """
        Make the bot shutdown
        """
        if ctx.message.author.id in config["owners"]:
            embed = discord.Embed(
                description="Shutting down. Bye! :wave:",
                color=config["success"]
            )
            await ctx.send(embed=embed)
            await self.bot.logout()
            await self.bot.close()
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=config["error"]
            )
            await ctx.send(embed=embed)

    @commands.command(name="say", aliases=["echo"])
    async def say(self, ctx, *, args):
        """
        The bot will say anything you want.
        """
        if ctx.message.author.id in config["owners"]:
            await ctx.send(args)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=config["error"]
            )
            await ctx.send(embed=embed)

    @commands.command(name="embed")
    async def embed(self, ctx, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        if ctx.message.author.id in config["owners"]:
            embed = discord.Embed(
                description=args,
                color=config["success"]
            )
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=config["error"]
            )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(owner(bot))
