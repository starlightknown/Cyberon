import discord
import datetime
from discord.ext import commands
import os, sys, discord, random, asyncio

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        result = await self.bot.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", member.guild.id)
        if result:
            members = len(list(member.guild.members))
            user = member.name
            mention = member.mention
            guild = member.guild.name

            embed = discord.Embed(colour=discord.Colour.green(), description=str(result["msg"]).format(members=members, mention=mention, guild=guild, user=user))

            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(id=int(result["channel_id"]))
            await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def welcome(self, context):
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Command Configuration", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Welcome Message Config Options:", value="f.welcome channel <#channel>\nf.welcome text <message>", inline=False)

        await context.send(embed=embed)

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def channel(self, context, channel:discord.TextChannel):
        result = await self.bot.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", context.guild.id)

        if not result:
            await self.bot.pg_con.execute("INSERT INTO welcome(guild_id, channel_id) VALUES($1,$2)", context.guild.id, channel.id)
            await context.send(f"The welcome channel has been set to {channel.mention}")

        else:
            await self.bot.pg_con.execute("UPDATE welcome SET channel_id = $1 WHERE guild_id = $2", channel.id, context.guild.id)
            await context.send(f"The welcome channel has been updated to {channel.mention}")

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def text(self, context, *, text):
        result = await self.bot.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", context.guild.id)

        if not result:
            await self.bot.pg_con.execute("INSERT INTO welcome(guild_id, msg) VALUES($1,$2)", context.guild.id, text)
            await context.send(f'The welcome message has been set to "{text}"')

        else:
            await self.bot.pg_con.execute("UPDATE welcome SET msg = $1 WHERE guild_id = $2", text, context.guild.id)
            await context.send(f'The welcome message has been updated to "{text}"')

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def check(self, context):
        result = await self.bot.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", context.guild.id)

        if not result:
            msg = "NONE"
            channel = "NONE"
        else:
            msg = "NONE" if not result["msg"] else result["msg"]
            channel = "NONE" if not result["channel_id"] else result["channel_id"]
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Command Configuration", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Welcome Message Config:", value=f'The welcome channel is set to <#{channel}>\nThe welcome text set to:\n\n"{msg}"', inline=False)

        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(welcome(bot))
