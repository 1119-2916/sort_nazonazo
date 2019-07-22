import discord
import sys
import random
import asyncio

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

def init_dictionary(src):
    dictionary = []
    try:
        dictionary_list_file = open(src, 'r')
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
dictionary = init_dictionary('dictionary_list')
print('dictionary size : ', len(dictionary))
if len(dictionary) == 0:
    print('problem not found')
    sys.exit()
extra_dictionary = init_dictionary('extra_dictionary_list')
print('extra_dictionary size : ', len(extra_dictionary))
token = read_token()
active_channel_id = read_active_channel_id()
lock = asyncio.Lock()


# status
question_solving = False
contest_solving = False
contest_problem_num = 0;
contest_solving_num = 0;
problem = ''
answer = ''

# 初期化
def hard_reset():
    global question_solving
    question_solving = False
    global contest_solving
    contest_solving = False
    global contest_problem_num
    contest_problem_num = 0
    global contest_solving_num
    contest_solving_num = 0
    global problem
    problem = ''
    global answer
    answer = ''

# コマンドを知るコマンドのパース
def cmd_list(cmd):
    if cmd.find('-cmd') != -1:
        print("cmd command is called")
        return True
    else:
        return False

# コマンドを知るコマンド
async def run_list(message):
    await message.channel.send(
"""
echo: -echo
出題: -prob
extra出題: -english
問題数を見る: -size
問題のヒントを見る: -hint NUM
問題を諦める: -giveup
連続で問題を出す: -contest NUM
連続で問題を出すのを中止する: -unrated
困った時は: -reset
botを落とす(再起動は出来ません): -bye
"""
)

# テスト用echoコマンドのパース
def cmd_echo(cmd):
    if cmd.find('-echo') != -1:
        print("echo command is called")
        return True
    else:
        return False
    
# テスト用echo関数
async def run_echo(message):
    await message.channel.send(message.content)

# 問題数を知るコマンドのパース
def cmd_problem_size(cmd):
    if cmd.find('-size') != -1:
        print("size command is called")
        return True
    else:
        return False

# 問題数を知るコマンド
async def run_problem_size(message):
    global dictionary
    await message.channel.send('全部で' + str(len(dictionary)) + '問あります')

# 問題を出題するコマンドのパース
def cmd_question(cmd):
    if cmd.find('-prob') != -1:
        print("prob command is called")
        return True
    else:
        return False

# 問題を出題するコマンド
async def run_question(message):
    global question_solving
    global contest_solving
    global contest_problem_num
    global contest_solving_num
    global dictionary
    global problem
    global answer
    if question_solving:
        await message.channel.send('前回の出題が解かれていません\n問題: ' + problem)
        return
    elif contest_solving:
        await message.channel.send('問 ' + str(contest_solving_num+1) + ' (' + str(contest_solving_num+1) + '/' + str(contest_problem_num) + ')')
        contest_solving_num += 1
    question_solving = True
    tmp = get_problem(dictionary)
    print(tmp)
    answer = tmp[0]
    problem = tmp[1]
    await message.channel.send('ソートなぞなぞ ソート前の文字列な〜んだ？\n' + problem)

# extra問題を出題するコマンドのパース
def cmd_extra_question(cmd):
    if cmd.find('-english') != -1:
        print("english command is called")
        return True
    else:
        return False

# extra問題を出題するコマンド
async def run_extra_question(message):
    global question_solving
    global contest_solving
    global contest_problem_num
    global contest_solving_num
    global extra_dictionary
    global problem
    global answer
    if question_solving:
        await message.channel.send('前回の出題が解かれていません\n問題: ' + problem)
        return
    elif contest_solving:
        await message.channel.send('問 ' + str(contest_solving_num+1) + ' (' + str(contest_solving_num+1) + '/' + str(contest_problem_num) + ')')
        contest_solving_num += 1
    question_solving = True
    tmp = get_problem(extra_dictionary)
    print(tmp)
    answer = tmp[0]
    problem = tmp[1]
    await message.channel.send('ソートなぞなぞ ソート前の文字列な〜んだ？\n' + problem)

# コンテストを出題するコマンドのパース
def cmd_contest(cmd):
    global contest_solving
    if cmd.find('-contest') != -1 and not contest_solving:
        print("prob command is called")
        return True
    else:
        return False

# コンテストを出題するコマンド
async def run_contest(message):
    global question_solving
    global contest_solving
    global contest_problem_num
    global problem
    contest_solving = True
    if question_solving:
        await message.channel.send('前回の出題が解かれていません\n問題: ' + problem)
        return
    contest_problem_num = 1
    for cmds in message.content.split(' '):
        print(cmds)
        if cmds.isdecimal():
            contest_problem_num = int(cmds)
            break
    if contest_problem_num > 50:
        await message.channel.send(str(contest_problem_num) + '問はちょっと多くない？50問にしますね。')
        contest_problem_num = 50
    if contest_problem_num <= 0:
        await message.channel.send(str(contest_problem_num) + '問の出題はできません。1問にしますね。')
        contest_problem_num = 1
    await message.channel.send(str(contest_problem_num) + '問連続で出題します。')
    await run_question(message)

# 問題解決処理後にコンテスト中なら出題を続行する
async def contest_continue(message):
    global contest_solving
    global contest_problem_num
    global contest_solving_num
    if not contest_solving:
        return 
    if contest_problem_num > contest_solving_num:
        await run_question(message)
    else:
        await message.channel.send(str(contest_problem_num) + '問連続の出題が終了しました。')
        contest_problem_num = 0
        contest_solving_num = 0
        contest_solving = False

# コンテストを中止するコマンドのパース
def cmd_unrated(cmd):
    global contest_solving
    if cmd.find('-unrated') != -1 and contest_solving:
        print("unrated command is called")
        return True
    else:
        return False

# コンテストを中止するコマンド
async def run_unrated(message):
    global contest_solving
    global contest_problem_num
    global contest_solving_num
    await message.channel.send(str(contest_problem_num) + '問連続の出題を中止します。')
    contest_solving_num = contest_problem_num
    contest_solving = False
    await run_giveup(message)
    contest_problem_num = 0
    contest_solving_num = 0

# 問題を諦めるコマンドのパース
def cmd_giveup(cmd):
    if cmd.find('-giveup') != -1:
        print("giveup command is called")
        return True
    else:
        return False

# 問題を諦めるコマンド
async def run_giveup(message):
    global question_solving
    global problem
    global answer
    if question_solving:
        response = '正解は\"' + answer + '\"でした...'
        await message.channel.send(response)
        question_solving = False
        problem = ''
        answer = ''
        await contest_continue(message)
    else:
        response = '現在問題は出されていません'
        await message.channel.send(response)

# 問題のヒントを出すコマンドのパース
def cmd_hint(cmd):
    if cmd.find('-hint') != -1:
        print("hint command is called")
        return True
    else:
        return False

# 問題のヒントを出すコマンド
async def run_hint(message):
    global question_solving
    global answer
    if not question_solving:
        response = '現在問題は出されていません'
        await message.channel.send(response)
        return
    hint_length = 1
    for cmds in message.content.split(' '):
        if cmds.isdecimal():
            hint_length = int(cmds)
            break
    #await message.channel.send(str(hint_length) + '文字ヒント:', end='');
    await message.channel.send(str(hint_length) + '文字ヒント:')
    if hint_length >= len(answer):
        await message.channel.send('答えが知りたい場合は -giveup を使用して下さい。')
        return
    if question_solving:
        response = '答えの先頭' + str(hint_length) + '文字は\"' + answer[0:hint_length] + '\"です'
        await message.channel.send(response)

# bot の状態を初期化するコマンドのパース
def cmd_reset(cmd):
    if cmd.find('-reset') != -1:
        print("reset command is called")
        return True
    else:
        return False

# bot の状態を初期化するコマンド
async def run_reset(message):
    hard_reset()
    await message.channel.send('botの状態を初期化しました。')

# bot を終了するコマンドのパース
def cmd_quit(cmd):
    if cmd.find('-bye') != -1:
        print("bye command is called")
        return True
    else:
        return False

# bot を終了するコマンド
async def run_quit(message):
    await message.channel.send('botを終了しました。')
    sys.exit()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# 待望の機能
def cmd_kick(cmd):
    if cmd.find('kick();') != -1:
        print("kick command is called")
        return True
    else:
        return False

# 待望のコマンド
async def run_kick(message):
    await message.channel.send('ヒィンｗ')

@client.event
async def on_message(message):
    global question_solving
    global problem
    global answer
    global lock
    if message.author == client.user:
        return
    if message.channel.id != active_channel_id:
        return
    if not client.user in message.mentions:
        await lock.acquire()
        if len(message.mentions) == 0 and question_solving and len(message.content) == len(problem):
            if message.content == answer:
                response = str(message.author) + ' さん、正解です！\n' + '正解は\"' + answer + '\"でした！'
                await message.channel.send(response)
                question_solving = False
                problem = ''
                answer = ''
                await contest_continue(message)
        lock.release()
        return 

    if cmd_echo(message.content):
        await run_echo(message)

    if cmd_list(message.content):
        await run_list(message)

    if cmd_problem_size(message.content):
        await run_problem_size(message)

    if cmd_reset(message.content):
        await run_reset(message)

    if cmd_hint(message.content):
        await run_hint(message)

    if cmd_giveup(message.content):
        await run_giveup(message)

    if cmd_question(message.content):
        await run_question(message)

    if cmd_extra_question(message.content):
        await run_extra_question(message)

    if cmd_contest(message.content):
        await run_contest(message)

    if cmd_unrated(message.content):
        await run_unrated(message)

    if cmd_kick(message.content):
        await run_kick(message)

    if cmd_quit(message.content):
        await run_quit(message)

client.run(token)
