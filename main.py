import os
import asyncio
import requests
import discord

from config import Config

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    url = os.path.join(Config.API_URL, 'text', message.content)
    response = requests.get(url)
    await message.channel.send(response.text)

client.run(Config.TOKEN)
