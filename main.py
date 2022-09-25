#using tutorial from https://www.youtube.com/watch?v=Vz67oGgdXoQ
import discord
import os
import requests
import json
from dotenv import load_dotenv
from weather import *


api_key = '62ce074edef864d4ded19169eb8920b2'
command_prefix = 'w.'
load_dotenv()
token = os.getenv('TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{command_prefix}[location]'))

@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(command_prefix):
        location = message.content.replace(command_prefix, '').lower()
        if len(location) >= 1:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))

client.run(token)