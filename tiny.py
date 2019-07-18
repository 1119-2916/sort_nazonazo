import discord
import sys

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

def read_active_channel_id():
    channel_id = -1
    try:
        channel_id_file = open('channel_id', 'r')
        channel_id = int(channel_id_file.read())
    except:
        print('failed to find or read channel id file. check your channel id file')
    finally:
        return channel_id

def init_dictionary():
    dictionary = []
    try:
        dictionary_list_file = open('dictionary_list', 'r')
        for dictionary_file_name in dictionary_list_file:
            print(dictionary_file_name.replace('\n',''), end='')
            try:
                dictionary_file = open(dictionary_file_name.replace('\n',''), 'r')
                print(' found')
                for sentence in dictionary_file:
                    dictionary.append(sentence.replace('\n','').split(' '))
            except:
                print(' NOT found')
    except:
        print('failed to find or read dictionary list file. check your dictionary list file')
    finally:
        return dictionary

# 問題数を知るコマンド
def cmd_problem_size(cmd):
    if cmd.find('-size'):
        print("size command is called")
        return True
    else:
        return False

# init
dictionary = init_dictionary()
print('dictionary size : ', len(dictionary))
if len(dictionary) == 0:
    print('problem not found')
    sys.exit()
token = read_token()
active_channel_id = read_active_channel_id()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id != active_channel_id:
        return
    if not client.user in message.mentions:
        print(message.mentions)
        return 

    if cmd_problem_size(message.content):
        await message.channel.send('全部で' + str(len(dictionary)) + '問あります')

client.run(token)
