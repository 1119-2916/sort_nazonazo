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
#print(str(bot.checkAnswer("hohoho")) + 'bot.checkAnswer("hohoho")')
#print(str(bot.endProblem()) + 'bot.endProblem()')
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

def getCmdList():
    return """
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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global lock
    if message.author == client.user:
        return
    if message.channel.id != active_channel_id:
        return

    await lock.acquire()
    if client.user in message.mentions:
        # コマンドのパース
        print(message.content)
        if len(message.content.split(' ')) > 1:
            cmd = message.content.split(' ')[1]
            cmdlist = message.content.split(' ')
            print('receive : ' + cmd)
            if cmd == '-echo':
                response = bot.echo(message.content)
                await message.channel.send(response)
            elif cmd == '-kick();':
                await message.channel.send('ヒィンｗ')
            elif cmd == '-bye':
                await run_quit(message)
            elif cmd == '-prob':
                if not bot.isGenerated():
                    bot.generateProblem()
                    print(bot.getProblem())
                    await message.channel.send('ソートなぞなぞ ソート前の文字列な〜んだ？\n' + bot.getProblem().problem)
                else:
                    await message.channel.send('前回の出題が解かれていません\n問題: ' + bot.getProblem().problem)
            elif cmd == '-giveup':
                if bot.isGenerated():
                    response = '正解は\"' + bot.getProblem().answer + '\"でした...'
                    await message.channel.send(response)
                    bot.endProblem()
                else:
                    response = '現在問題は出されていません'
                    await message.channel.send(response)
            elif cmd == '-dic':
                response = '現在の辞書の状態は以下です\n'
                state = bot.getAllDicStatus()
                for i in state:
                    response += '辞書名 : ' + i[0] + ' , 問題数 : ' + str(i[1]) + ' , 出題対象 : ' + str(i[2]) + '\n'
                await message.channel.send(response)
            elif cmd == '-hint':
                print('log : hint call')
                if not bot.isGenerated():
                    response = '現在問題は出されていません'
                    await message.channel.send(response)
                elif len(cmdlist) != 3:
                    response = 'ヒントは \"-hint NUM \" の形式でのみ応答します'
                    await message.channel.send(response)
                elif cmdlist[2] == 'NUM':
                    response = 'NUM って言ったけどそうではなくて、数字を入れて下さい'
                    await message.channel.send(response)
                else:
                    try:
                        hint_length = int(cmdlist[2])
                        if hint_length < 0:
                            response = str(hint_length) + '文字のヒントは出せません…'
                            await message.channel.send(response)
                        elif hint_length > len(bot.getProblem().problem):
                            response = str(hint_length) + '文字のヒントは出せません…\n答えが知りたい場合は -giveup コマンドを使用して下さい。'
                            await message.channel.send(response)
                        else:
                            response = str(hint_length) + '文字のヒント:\n'
                            response += '答えの先頭' + str(hint_length) + '文字は\"' + bot.getProblem().answer[0:hint_length] + '\"です'
                            await message.channel.send(response)
                    except:
                        response = 'NUM の部分には数字を入れて下さい'
                        await message.channel.send(response)

    elif bot.isGenerated(): # 答えの確認
        if bot.checkAnswer(message.content, str(message.author)):
            win = bot.getWinnter()
            response = win[0] + ' さん、正解です！\n' + '正解は\"' + message.content + '\"でした！'
            await message.channel.send(response)
            bot.endProblem()
        elif bot.checkAnotherAnswer(message.content, str(message.author)):
            response = str(message.author) + ' さん、 \"' + message.content + '\" は非想定解ですが正解です！'
            await message.channel.send(response)

    lock.release()

client.run(token)
