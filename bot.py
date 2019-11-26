import os

import discord
from dotenv import load_dotenv

load_dotenv("./discord.env")
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


@client.event
async def on_ready():
    print('discord bot ready..')
    print(
        f'{client.user} is connected.:\n'
    )


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

client.run(TOKEN)