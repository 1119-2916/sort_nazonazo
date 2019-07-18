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

# コマンドを知るコマンド
def cmd_list(cmd):
    if cmd.find('-cmd') != -1:
        print("cmd command is called")
        return True
    else:
        return False

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

# 問題を諦めるコマンド
def cmd_giveup(cmd):
    if cmd.find('-giveup') != -1:
        print("giveup command is called")
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
        if len(message.mentions) == 0 and question_solving and len(message.content) == len(problem):
            if message.content == answer:
                response = str(message.author) + ' さん、正解です！\n' + '正解は\"' + answer + '\"でした！'
                await message.channel.send(response)
                question_solving = False
                problem = ''
                answer = ''
            # else :
                # todo : 別解を保持する処理
                # todo : WA を判定して粋な emoji を打つ
        return 

    if cmd_list(message.content):
        await message.channel.send('出題: -prob\n問題数を見る: -size\n問題を諦める: -giveup\n困った時は: -reset')

    if cmd_problem_size(message.content):
        await message.channel.send('全部で' + str(len(dictionary)) + '問あります')

    if cmd_reset(message.content):
        hard_reset()
        await message.channel.send('botの状態を初期化します')

    if cmd_giveup(message.content):
        if question_solving:
            response = '正解は\"' + answer + '\"でした...'
            await message.channel.send(response)
            question_solving = False
            problem = ''
            answer = ''
        else:
            response = '現在問題は出されていません'
            await message.channel.send(response)

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
