import json
import os
import platform
import random
import sys

import aiohttp
import discord
import yaml
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="love-ya")
    async def _love(self, ctx: commands.Context):
        await ctx.message.add_reaction(":gift_heart:")
        await ctx.send("You are the best! :heart:")
    
    @commands.command(name="poll")
    async def poll(self, ctx, *args):
        """
        Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Poll created by: {ctx.message.author} • React to vote!"
        )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *args):
        """
        Ask any question to the bot.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Question asked by: {ctx.message.author}"
        )
        await ctx.send(embed=embed)

    @commands.command(name="bitcoin")
    async def bitcoin(self, ctx):
        """
        Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=config["success"]
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
