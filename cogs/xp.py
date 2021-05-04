import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import random,os,sys

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!', '@', '#', '$', '%', '^', '&', '(', ')']

class randomxp(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.xpEvent.start()

  @tasks.loop(minutes=60.0)
  async def xpEvent(self):
    await self.bot.wait_for("message", timeout=60.0)

    genChannel = self.bot.get_channel(832950556100132874)
    logChannel = self.bot.get_channel(839128592507863062)
    randomN = random.randint(0, 3)

    if randomN == 0:
      xpAmount = random.randint(1000, 15000)

      code = []

      for i in range(0, 10):
        randomN = random.randint(0, len(chars) - 1)
        code.append(chars[randomN])

      code = "".join(code)

      await genChannel.trigger_typing()
      await genChannel.send(f"""
      **XP EVENT**
      The first person to send **{code}** gets {xpAmount} XP!
      """)

      def check(msg):
        return msg.channel == genChannel and msg.content == code

      msg = await self.bot.wait_for("message", check=check, timeout=60.0)

      winner = msg.author

      await genChannel.trigger_typing()
      await logChannel.send(f"{winner} has earned {xpAmount} XP")
      await genChannel.send(f"Congrats {winner.mention}! You have won {xpAmount} XP!")

  @commands.command()
  @has_permissions(manage_channels=True)
  async def testxp(self, ctx):
    logChannel = self.bot.get_channel(839128592507863062)

    xpAmount = random.randint(1000, 15000)

    code = []

    for i in range(0, 10):
      randomN = random.randint(0, len(chars))
      code.append(chars[randomN])

    code = "".join(code)

    await ctx.send(f"""
    **XP EVENT**
    The first person to send **{code}** gets {xpAmount} XP!
    """)

    def check(msg):
      return msg.content == code

    msg = await self.bot.wait_for("message", check=check)

    winner = msg.author

    await logChannel.send(f"{winner} has earned {xpAmount} XP")
    await ctx.send(f"Congrats {winner.mention}! You have won {xpAmount} XP!")

def setup(bot):
  bot.add_cog(randomxp(bot))

