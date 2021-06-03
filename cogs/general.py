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
    @commands.command()
    async def xkcd(self, ctx,  *searchterm: str):
        ''' XKCD Comic
        -----------
        cyb!xkcd random
        '''
        apiUrl = 'https://xkcd.com{}info.0.json'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(apiUrl.format('/')) as r:
                js = await r.json()
                if ''.join(searchterm) == 'random':
                    randomComic = random.randint(0, js['num'])
                    async with cs.get(apiUrl.format('/' + str(randomComic) + '/')) as r:
                        if r.status == 200:
                            js = await r.json()
                comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
                date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
                msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(js['safe_title'], js['img'], js['alt'], comicUrl, date)
                await ctx.send(msg)

    @commands.command(name="decide")
    async def _decide(self, ctx: commands.Context, *, to_decide: str):
        """Decide between a list of comma separated options"""
        options = [x.strip() for x in to_decide.split(",")]
        choice = random.choice(options)

        await ctx.send(
            embed=discord.Embed(color=discord.Color.blurple(), description=choice)
        )

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

    @commands.command(name="lovin")
    async def love(self, ctx: commands.Context, *, target=None):
        """ Give someone some lovin' """

        if not target:
            return await ctx.send(f"{ctx.author.display_name} loves ... nothing")

        await ctx.send(
            f":heart_decoration: {ctx.author.display_name} gives {target} some good ol' fashioned lovin'. :heart_decoration:"
        )

    @commands.command(aliases=["at"])
    async def aesthetify(self, ctx: commands.Context, *, a_text):
        """ Make your message ａｅｓｔｈｅｔｉｃ，　ｍａｎ """
        ascii_to_wide = {i: chr(i + 0xFEE0) for i in range(0x21, 0x7F)}
        ascii_to_wide.update({0x20: "\u3000", 0x2D: "\u2212"})

        await ctx.message.delete()
        await ctx.send(f"{a_text.translate(ascii_to_wide)}")

    @commands.command(name="boop")
    async def boop(self, ctx: commands.Context, *, target=None):
        """ boop someone """
        if target is None:
            return await ctx.send(
                f"{ctx.author.name} started running behind to boop."
            )

        embed = discord.Embed(description = f'**{ctx.author.name} booped {target} finally, how cute!**')
        embed.set_image(url = 'https://media.giphy.com/media/10MSCF1viNV7zy/giphy.gif')
        await ctx.send(embed = embed)

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
