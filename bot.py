import os
import pickle
from googleapiclient.discovery import build
import discord
from dotenv import load_dotenv


load_dotenv("./discord.env")
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
my_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
my_cse_id = os.getenv('SEARCH_ENGINE_ID')

SEARCH_HISTORY = {}

def google_search(search_term, api_key=my_api_key, cse_id=my_cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def google_search_top_5_as_string_message(search_term):
    res = google_search(search_term)
    msg = ''
    for ind, item in enumerate(res['items']):
        if ind == 5:
            break
        _msg = '{s_no}-{title}, {link}\n'.format(s_no=ind+1, title=item['title'], link=item['link'])
        msg += _msg
    return msg


@client.event
async def on_ready():
    print('discord bot ready..')


def save_history():#EXTREMELY SLOW, just for testing
    with open('search_history', 'wb') as f:
        pickle.dump(SEARCH_HISTORY, f)


def load_history():
    global SEARCH_HISTORY
    try:
        with open('search_history', 'rb') as f:
            SEARCH_HISTORY = pickle.load(f)
    except FileNotFoundError:
        save_history()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    print('MESSAGE AUTHOR', message.author)
    if message.author == client.user:
        return
    if message.content == 'hey':
        print('Hey found')
        await message.channel.send("hi")

    elif message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    elif message.content.startswith('!google'):
        broken_msg = message.content.split('!google')
        print('BROKEN_MESSAGE', broken_msg)
        search_q = broken_msg[1].replace('"', '')
        print('SEARCH QUERY', search_q)
        msg = google_search_top_5_as_string_message(search_q)
        print('SEARCH RESULT', msg)
        if not SEARCH_HISTORY.get(message.author.name):
            SEARCH_HISTORY[message.author.name] = []
        SEARCH_HISTORY[message.author.name].append(search_q)
        save_history()
        print('history saved'.upper())
        await message.channel.send(msg)

    elif message.content.startswith("!recent"):
        broken_msg = message.content.split()
        print('BROKEN_MESSAGE', broken_msg)
        rt_message = ''
        history = SEARCH_HISTORY[message.author.name]
        if len(broken_msg) > 1:
            match_with = broken_msg[1]
        else:
            match_with = None
        for el in history:
            if match_with:
                if match_with in el:
                    rt_message += el + ' \n'
            else:
                rt_message += el + ' \n'
        await message.channel.send(rt_message)

load_history()

if __name__ == '__main__':
    client.run(TOKEN)
