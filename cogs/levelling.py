import discord
from discord.ext import commands
import sqlite3
from random import randint
import yaml
import os, sys
bot_id= 819568634673889341
if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        
        if message.author.id is bot_id:
            pass
        else:
            totalMessages = 1
            newLevel = 0
            newExperience = 0
            dbconnect = sqlite3.connect('users.db')
            cursor = dbconnect.cursor()
            records = cursor.execute("SELECT username, messages, level, experience FROM messagecounts WHERE username = ?", [str(member)]).fetchall()
            for row in records:
                totalMessages = row[1] + 1
                addOnXP = randint(10, 20)
                newExperience = row[3] + addOnXP
                newLevel = round(newExperience, -3) / 1000
                if newLevel > row[2]:
                    await message.channel.send(f"Level Up! {message.author} is level {int(newLevel)}")
            cursor.execute("SELECT username, messages, level, experience FROM messagecounts WHERE username = ?", [str(member)])
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE messagecounts SET messages = ? WHERE username = ?", [totalMessages, str(member)])
                cursor.execute("UPDATE messagecounts SET level = ? WHERE username = ?", [newLevel, str(member)])
                cursor.execute("UPDATE messagecounts SET experience = ? WHERE username = ?", [newExperience, str(member)])
            else:
                cursor.execute('''INSERT INTO messagecounts(username, messages, level, experience) VALUES(?,?,?,?)''', (str(member), totalMessages, 0, 0))
            dbconnect.commit()
            dbconnect.close()

    @commands.command()
    async def level(self, ctx):
        dbconnect = sqlite3.connect('users.db')
        cursor = dbconnect.cursor()
        userData = cursor.execute("SELECT username, messages, level, experience FROM messagecounts WHERE username = ?", [str(ctx.message.author)]).fetchall()
        for item in userData:
            userLevel = item[2]
            userExperience = item[3]
            userMessages = item[1]
            userName = item[0]
            embedVar = discord.Embed(title="LEVEL:", description=f"For: **{userName}**", color=0xf1c40f)
            embedVar.add_field(name="Messages:", value=f"**{userMessages}**", inline=True)
            embedVar.add_field(name="Experience:", value=f"**{userExperience}**", inline=True)
            embedVar.add_field(name="Level:", value=f"**{userLevel}**", inline=True)
            await ctx.send(embed=embedVar)

    @commands.command()
    async def leaderboard(self, ctx):
        dbconnect = sqlite3.connect('users.db')
        cursor = dbconnect.cursor()
        userData = cursor.execute("SELECT * FROM messagecounts ORDER BY experience DESC LIMIT 3").fetchall()
        embedVar = discord.Embed(title="LEADERBOARD:", description="Top 3 members in the guild!", color=0xf1c40f)
        for item in userData:
            userLevel = item[2]
            userExperience = item[3]
            userMessages = item[1]
            userName = item[0]
            embedVar.add_field(name="User:", value=f"**{userName}**: {userExperience} experience, {userLevel} levels, {userMessages} messages!", inline=False)
        await ctx.send(embed=embedVar)
        dbconnect.commit()
        dbconnect.close()

def setup(bot):
    bot.add_cog(Levelling(bot))
