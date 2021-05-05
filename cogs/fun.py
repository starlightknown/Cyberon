import os, sys, discord, random, asyncio
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="green-squares")
    async def green_squares(self, context, member : discord.Member = None):
        ''' 
        Check your love for open source 
        '''
        if not member:
            member = context.author
        length = random.randrange(15)

        embed = discord.Embed(description=f"{':green_square: :heart: '*length} You rock!", color=config.main_color)
        embed.set_author(name=f"{member.display_name}'s love for green squares", icon_url=member.avatar_url)
        await context.send(embed=embed)

    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        choices = {
            0 : "rock",
            1 : "paper",
            2 : "scissors"
        }
        reactions = {
            "🪨" : 0,
            "🧻" : 1,
            "✂" : 2
        }
        embed = discord.Embed(title="Please choose", color=config.warning)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=config.success)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config.warning
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config.success
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config.success
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config.success
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config.error
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(
                    title='Too Late',
                    description="It's never too late to play again ;) ",
                    colour=0xff0000)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)

    @commands.command(name="8ball")
    async def eight_ball(self, context, *args):
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
            color=config.success
        )
        embed.set_thumbnail(url = 'https://media.giphy.com/media/vSShDn9lRdC2OJnh24/giphy.gif')
        embed.set_footer(
            text=f"Question asked by: {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="boop")
    async def boop(self, context, member: discord.Member, *args):
        embed = discord.Embed(description = f'**{context.author.mention} booped {member.mention}**')
        embed.set_image(url = 'https://media.giphy.com/media/10MSCF1viNV7zy/giphy.gif')
        await context.send(embed = embed)


def setup(bot):
    bot.add_cog(Fun(bot))
