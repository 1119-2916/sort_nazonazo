import discord
import sys
import random
from sort_nazonazo_bot import SortNazonazoBot
import asyncio

client = discord.Client()

def read_token():
    token = ''
    try:
        token_file = open('../key/token', 'r')
        token = token_file.read().replace('\n','')
    except:
        print('failed to find or read token file. check your token file')
    finally:
        return token

def read_active_channel_id():
    channel_id = -1
    try:
        channel_id_file = open('../key/channel_id', 'r')
        channel_id = int(channel_id_file.read())
    except:
        print('failed to find or read channel id file. check your channel id file')
    finally:
        return channel_id

#bot = test('dictionary_list')
#print(bot.getAllDicStatus())
#print(bot.getDicNameList())
#bot.setDicSelected(bot.getDicNameList()[0], False)
#print(bot.getAllDicStatus())
#bot.setDicSelected(bot.getDicNameList()[0], True)
#bot.resetDicSelected()
#print(bot.getAllDicStatus())
#bot.selectAllDic()
#print(str(bot.getAllDicStatus()) + 'bot.getAllDicStatus()')
#print(str(bot.generateProblem()) + 'bot.generateProblem()')
#print(str(bot.isGenerated()) + 'bot.isGenerated()')
#print(str(bot.getProblem()) + 'bot.getProblem()')
#print(str(bot.generateProblem()) + 'bot.generateProblem()')
#print(str(bot.isGenerated()) + 'bot.isGenerated()')
#print(str(bot.sendAnswer("hohoho")) + 'bot.sendAnswer("hohoho")')
#print(str(bot.clearProblem()) + 'bot.clearProblem()')
#print(str(bot.isGenerated()) + 'bot.isGenerated()')

# init
bot = SortNazonazoBot()
bot.readDictionaries('dictionary_list')
#print('dictionary size : ', len(dictionary))
print('dictionary info : ')
print(bot.getAllDicStatus())
num = 0
for i in bot.getDicNameList():
    print('loaded dic name : ' + i)
    num += bot.getDicSize(i)
if num == 0:
    print('problem not found')
    sys.exit()
token = read_token()
active_channel_id = read_active_channel_id()
lock = asyncio.Lock()

# コマンドを知るコマンドのパース
def cmd_list(cmd):
    if cmd.find('-cmd') != -1:
        print("cmd command is called")
        return True
    else:
        return False

# テスト用echoコマンドのパース
def cmd_echo(cmd):
    if cmd.find('-echo') != -1:
        print("echo command is called")
        return True
    else:
        return False

# 問題数を知るコマンドのパース
def cmd_problem_size(cmd):
    if cmd.find('-size') != -1:
        print("size command is called")
        return True
    else:
        return False

# 問題を出題するコマンドのパース
def cmd_question(cmd):
    if cmd.find('-prob') != -1:
        print("prob command is called")
        return True
    else:
        return False

# extra問題を出題するコマンドのパース
def cmd_extra_question(cmd):
    if cmd.find('-english') != -1:
        print("english command is called")
        return True
    else:
        return False

# コンテストを出題するコマンドのパース
def cmd_contest(cmd):
    global contest_solving
    if cmd.find('-contest') != -1 and not contest_solving:
        print("prob command is called")
        return True
    else:
        return False

# コンテストを中止するコマンドのパース
def cmd_unrated(cmd):
    global contest_solving
    if cmd.find('-unrated') != -1 and contest_solving:
        print("unrated command is called")
        return True
    else:
        return False


# 問題を諦めるコマンドのパース
def cmd_giveup(cmd):
    if cmd.find('-giveup') != -1:
        print("giveup command is called")
        return True
    else:
        return False


# 問題のヒントを出すコマンドのパース
def cmd_hint(cmd):
    if cmd.find('-hint') != -1:
        print("hint command is called")
        return True
    else:
        return False

# bot の状態を初期化するコマンドのパース
def cmd_reset(cmd):
    if cmd.find('-reset') != -1:
        print("reset command is called")
        return True
    else:
        return False

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
    if message.author == client.user:
        return
    if message.channel.id != active_channel_id:
        return

    await lock.acquire()

    if cmd_kick(message.content):
        await run_kick(message)

    if cmd_quit(message.content):
        await run_quit(message)

    lock.release()

client.run(token)
