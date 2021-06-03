import asyncio
import os
import random
import sys
import aiohttp
import discord
import yaml
from discord.ext import commands
from discord.ext.commands import BucketType

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class fun(commands.Cog, name="cybgames"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cat', 'randomcat'])
    async def randcat(self, ctx):
        '''gets you a random cat~'''
        #http://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                res = await r.json()
                emojis = [':cat2: ', ':cat: ', ':heart_eyes_cat: ']
                await ctx.send(random.choice(emojis) + res['file'])
  
    @commands.command(name="8ball", aliases=["ball"])
    async def ball(self, ctx: commands.Context, *, query=None):
        """ Ask the magic 8ball """
        if query is None:
            return await ctx.error("The 8Ball's wisdom is not to be wasted.")

        responses = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
        ]

        if not query.endswith("?"):
            query = f"{query}?"

        await ctx.send(
            embed=discord.Embed(
                title=f":8ball: {query}",
                description=random.choice(responses),
                color=self.blue,
            )
        )

    @commands.command()
    async def same(self, ctx):
        await ctx.send(":white_check_mark: same\n:green_square: unsame")

    @commands.command()
    async def unsame(self, ctx):
        await ctx.send(":green_square: same\n:white_check_mark: unsame")

    @commands.command()
    async def resame(self, ctx):
        await ctx.send(
            ":white_check_mark: same\n:white_check_mark: re:same\n:green_square: unsame"
        )

    @commands.command(name="dailyfact")
    @commands.cooldown(1, 86400, BucketType.user)
    async def dailyfact(self, ctx):
        """
        Get a daily fact, command can only be ran once every day per user.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=config["main_color"])
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=config["error"]
                    )
                    await ctx.send(embed=embed)
                    # We need to reset the cool down since the user didn't got his daily fact.
                    self.dailyfact.reset_cooldown(ctx)

    @commands.command(name="rps")
    async def rock_paper_scissors(self, ctx):
        """play rock paper scissors"""
        choices = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Please choose", color=config["warning"])
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        choose_message = await ctx.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=config["success"])
            result_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["warning"]
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["success"]
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["success"]
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["success"]
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["error"]
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=config["error"])
            timeout_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)


def setup(bot):
    bot.add_cog(fun(bot))
