import discord

active_channel = 'sort_nazonazo'
client = discord.Client()

def read_token():
    token = ''
    try:
        token_file = open('token', 'r')
        token = token_file.read().replace('\n','')
    except:
        print('failed to find or read token file. check your token file')
    finally:
        return token

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send(active_channel, 'Hello!')

client.run(read_token())
