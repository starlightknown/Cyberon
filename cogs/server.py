import os
import sys
from datetime import datetime, timedelta
import discord
import yaml
from discord.ext import commands

# Only if you want to use variables that are in the config.yaml file.
if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

class serverinfo(commands.Cog, name="server"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        """
        Get some useful (or not) information about the server.
        """
        server = ctx.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=config["success"]
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"{server.owner}\n{server.owner.id}"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await ctx.send(embed=embed)

    @commands.command(name="user-messages")
    async def check(self, context, timeframe=7, channel: discord.TextChannel = None, *, user: discord.Member = None):
        if timeframe > 1968:
            await context.channel.send("Sorry. The maximum of days you can check is 1968.")
        elif timeframe <= 0:
            await context.channel.send("Sorry. The minimum of days you can check is one.")

        else:
            if not channel:
                channel = context.channel
            if not user:
                user = context.author

            async with context.channel.typing():
                msg = await context.channel.send('Calculating...')
                await msg.add_reaction('🔎')

                counter = 0
                async for message in channel.history(limit=5000, after=datetime.today() - timedelta(days=timeframe)):
                    if message.author.id == user.id:
                        counter += 1

                await msg.remove_reaction('🔎', member=message.author)

                if counter >= 5000:
                    await msg.edit(content=f'{user} has sent over 5000 messages in the channel "{channel}" within the last {timeframe} days!')
                else:
                    await msg.edit(content=f'{user} has sent {str(counter)} messages in the channel "{channel}" within the last {timeframe} days.')

    @commands.command(name="ping")
    async def ping(self, ctx):
        """See the bot's latency"""
        latency = ctx.bot.latency * 1000
        embed = discord.Embed(
            title=":ping_pong: Pong!",
            description=f"**Bot latency:** ```{latency:.2f} ms```",
            color=config["main_color"]
        )
        await ctx.send(embed=embed)

    @commands.command(name="user")
    async def whois(self, ctx, member: discord.Member = None):
        """get info about a user in server"""
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.orange(), timestamp=ctx.message.created_at,
                              title=str(member))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="ID:", value=member.id)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(
            name="Roles:", value="".join(role.mention for role in roles[1:])
        )

        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)


    @commands.command(name="server")
    async def server(self, ctx):
        """
        Get the invite link of the discord server of the bot for some support.
        """
        await ctx.send("I sent you a private message!")
        await ctx.author.send("Join my discord server by clicking here: https://discord.gg/HzJ3Gfr")

def setup(bot):
    bot.add_cog(serverinfo(bot))