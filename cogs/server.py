import os
import sys
import discord
import yaml
from discord.ext import commands

# Only if you want to use variables that are in the config.yaml file.
if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

class ServerInfo(commands.Cog, name="Server"):
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

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
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
    bot.add_cog(ServerInfo(bot))