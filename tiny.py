import discord
import sys
import random

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

# 辞書から問題を1問取ってくる
def get_problem(dictionary):
    return dictionary[random.randrange(len(dictionary))]

# init
dictionary = init_dictionary()
print('dictionary size : ', len(dictionary))
if len(dictionary) == 0:
    print('problem not found')
    sys.exit()
token = read_token()
active_channel_id = read_active_channel_id()
question_solving = False
problem = ''
answer = ''

# 初期化
def hard_reset():
    global question_solving
    question_solving = False
    global problem
    problem = ''
    global answer
    answer = ''

# 問題数を知るコマンド
def cmd_problem_size(cmd):
    if cmd.find('-size') != -1:
        print("size command is called")
        return True
    else:
        return False

# 問題を出題するコマンド
def cmd_question(cmd):
    if cmd.find('-prob') != -1:
        print("prob command is called")
        return True
    else:
        return False

# bot の状態を初期化するコマンド
def cmd_reset(cmd):
    if cmd.find('-reset') != -1:
        print("reset command is called")
        return True
    else:
        return False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global question_solving
    global dictionary
    global problem
    global answer
    if message.author == client.user:
        return
    if message.channel.id != active_channel_id:
        return
    if not client.user in message.mentions:
        print(message.mentions)
        return 

    if cmd_problem_size(message.content):
        await message.channel.send('全部で' + str(len(dictionary)) + '問あります')

    if cmd_reset(message.content):
        hard_reset()
        await message.channel.send('botの状態を初期化します')

    if cmd_question(message.content):
        if question_solving:
            await message.channel.send('前回の出題が解かれていません')
        else:
            question_solving = True
            tmp = get_problem(dictionary)
            print(tmp)
            answer = tmp[0]
            problem = tmp[1]
            print(type(problem))
            await message.channel.send('ソートなぞなぞ ソート前の文字列な〜んだ？\n' + problem)

client.run(token)
