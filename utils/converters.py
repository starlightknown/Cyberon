import datetime
import re
import discord
from discord.ext import commands

class TextChannelMention(commands.Converter):
    """A converter for checking if an argument is a text channel mention."""
    
    async def convert(self, ctx, argument):
        """Checks whether the argument is a text channel mention."""
        match = re.match(r'<#([0-9]+)>$', argument)
        if match is None:
            raise commands.BadArgument(f'{argument} is not a text channel mention')
        
        channel = ctx.guild.get_channel(int(match.group(1)))
        if channel is None:
            raise commands.BadArgument(f'Channel {argument} not found')
        
        return channel

class Duration(commands.Converter):
    """Represents a duration of time in seconds and the datetime when the duration ends."""
    
    def __init__(self, seconds=0, end=datetime.datetime.utcnow()):
        self.seconds = seconds
        self.end = end

    @classmethod
    async def convert(cls, ctx, argument):
        """
        Converts the argument into a Duration object.
        The argument can be specified in weeks, days, hours, minutes, and/or seconds.
        Durations can only be under 10 weeks.
        """
        match = re.fullmatch(r"""(?:(?P<weeks>\d)w)?                # ex: 5w
                                 (?:(?P<days>[0-6])d)?              # ex: 3d
                                 (?:(?P<hours>\d|1\d|2[0-3])h)?     # ex: 12h
                                 (?:(?P<minutes>\d|[1-5]\d)m)?      # ex: 30m
                                 (?:(?P<seconds>\d|[1-5]\d)s)?      # ex: 15s
                              """, argument, re.VERBOSE)
        
        if match is None or not match.group(0):
            raise commands.BadArgument('The duration for the reminder is not in the correct format or is not under 10 weeks')

        data = { interval: int(num) for interval, num in match.groupdict(default=0).items() }
        delta = datetime.timedelta(**data)
        seconds = int(delta.total_seconds())
        end = ctx.message.created_at + delta
        
        return cls(seconds, end)

    @staticmethod
    def display(seconds, granularity=5):
        """
        Displays the number of seconds in weeks, days, hours, minutes, and seconds.
        Examples:
            5440 seconds -> "1 hour 30 minutes 40 seconds"
            7201 seconds -> "2 hours 1 second"
        """
        conversions = (
            ('weeks', 604800),  # 1 week = 604800 seconds
            ('days', 86400),    # 1 day  = 86400 seconds
            ('hours', 3600),    # 1 hour = 3600 seconds
            ('minutes', 60), 
            ('seconds', 1)
        )

        result = []
        for interval, value in conversions:
            num = seconds // value
            if num:
                seconds -=  num * value
                if num == 1:
                    interval = interval.rstrip('s')
                result.append(f'{num} {interval}')

        return ' '.join(result[:granularity])