import discord
from discord.embeds import Embed
import random

color = 0xFF6500
key_features = {
    'title' : 'Name',
    'url':'Website',
    'time_left_to_submission': 'Start Time',
    'submisson_period_dates': 'End Time',
    'featured' : 'Featured?',
    'prize_amount' : 'Prize Amount'
}

def parse_data(data):
    del data['id']
    del data['displayed_location']
    del data['thumbnail_url']
    del data['themes']
    del data['registrations_count']
    del data['organisation_name']
    del data['winners_announced']
    del data['submission_gallery_url']
    del data['start_a_submission_url']
    return data

def hack_message(data):
    message = discord.Embed(
        title = f"Devpost Hackthon Details",
        description = "Here is the data for the latest Hackathon live on Devpost.",
        color = color,   
    )
    message.add_field(
    name = key_features['title'],
    value= data['title'],
    inline = False
    )
    message.add_field(
    name = key_features['url'],
    value= data['url'],
    inline = False
    )
    message.add_field(
    name = key_features['time_left_to_submission'],
    value=data['time_left_to_submission'],
    inline = False
    )
    message.add_field(
    name = key_features['submisson_period_dates'],
    value= data['submisson_period_dates'],
    inline = False
    )
    message.add_field(
    name = key_features['featured'],
    value= data['featured'],
    inline = False
    )
    message.add_field(
    name = key_features['prize_amount'],
    value= data['prize_amount'],
    inline = False
    )

    return message

def error_message():
    return discord.Embed(
        title = "Error",
        description = "Sorry an error occured",
        color  = color
    )