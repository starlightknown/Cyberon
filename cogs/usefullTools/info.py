import discord
from discord.embeds import Embed
import random

color = 0xFF6500
key_features = {
    'name' : 'Name',
    'website':'Website',
    'start': 'Start Time',
    'end': 'End Time',
    'city': 'City',
    'state':'State',
    'country': 'Country',
    'virtual':'Virtual Hack?',
    'mlhAssociated':'MLH Partnered?'
}

def parse_data(data):
    del data['id']
    del data['createdAt']
    del data['logo']
    del data['banner']
    del data['countryCode']
    del data['latitude']
    del data['longitude']
    return data

def hack_message(data):
    message = discord.Embed(
        title = f"Hack Club Hackthon Details",
        description = "Here is the data for the latest Hackathon live on The Hack Club.",
        color = color,   
    )
    message.set_thumbnail(url = 'https://assets.hackclub.com/icon-rounded.png')
    message.add_field(
    name = key_features['name'],
    value= data['name'],
    inline = False
    )
    message.add_field(
    name = key_features['website'],
    value= data['website'],
    inline = False
    )
    message.add_field(
    name = key_features['start'],
    value=data['start'],
    inline = False
    )
    message.add_field(
    name = key_features['end'],
    value= data['end'],
    inline = False
    )
    message.add_field(
    name = key_features['virtual'],
    value= data['virtual'],
    inline = False
    )
    message.add_field(
    name = key_features['mlhAssociated'],
    value= data['mlhAssociated'],
    inline = False
    )

    return message

def error_message():
    return discord.Embed(
        title = "Error",
        description = "Sorry an error occured",
        color  = color
    )