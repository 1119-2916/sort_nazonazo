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
# init
bot = SortNazonazoBot()
bot.readDictionaries('dictionary_list')
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

# bot を終了するコマンド
async def run_quit(message):
    await message.channel.send('botを終了しました。')
    sys.exit()

# 問題のヒントを得る
async def run_hint(message):
    cmdlist = message.content.split(' ')
    if not bot.isGenerated():
        response = '現在問題は出されていません'
        await message.channel.send(response)
    elif len(cmdlist) != 3:
        response = 'ヒントは \"-hint NUM \" の形式でのみ応答します'
        await message.channel.send(response)
    elif cmdlist[2] == 'NUM':
        response = 'NUM って言ったけどそうではなくて、NUM の部分には数字を入れて下さい'
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
        except ValueError:
            response = 'ヒントは \"-hint NUM \" の形式でのみ応答します\n'
            response += 'NUM の部分には数字を入れて下さい'
            await message.channel.send(response)

# 辞書を選択する
async def run_select(message):
    cmdlist = message.content.split(' ')
    if len(cmdlist) != 3:
        response = '辞書選択は \"-dic-select DIC_NAME \" の形式でのみ応答します\nDIC_NAMEには対象の辞書名を入れて下さい。辞書名の取得は -dic-status で可能です。'
        await message.channel.send(response)
    elif cmdlist[2] in bot.getDicNameList():
        bot.setDicSelected(cmdlist[2], True)
        response = '辞書 \"' + cmdlist[2] + '\" を出題対象にします。'
        await message.channel.send(response)
    else:
        response = '\"' + cmdlist[2] + '\" という名前の辞書はありません。'
        await message.channel.send(response)

# 辞書を選択解除する
async def run_deselect(message):
    cmdlist = message.content.split(' ')
    if len(cmdlist) != 3:
        response = '辞書選択は \"-dic-deselect DIC_NAME \" の形式でのみ応答します\nDIC_NAMEには対象の辞書名を入れて下さい。辞書名の取得は -dic-status で可能です。'
        await message.channel.send(response)
    elif cmdlist[2] in bot.getDicNameList():
        bot.setDicSelected(cmdlist[2], False)
        response = '辞書 \"' + cmdlist[2] + '\" を出題対象から外します。'
        await message.channel.send(response)
    else:
        response = '\"' + cmdlist[2] + '\" という名前の辞書はありません。'
        await message.channel.send(response)

# コンテストの問題を出す
async def run_contest_problem(message):
    if bot.isGenerated():
        await message.channel.send('前回の出題が解かれていません\n問題: ' + bot.getProblem().problem)
    elif not bot.contestRunning():
        await message.channel.send('コンテスト中ではありません。')
    else:
        if bot.generateContestProblem():
            print(bot.getProblem())
            now = str(bot.get_contest_problem_num() - bot.get_contest_problem_count() + 1)
            await message.channel.send('問 ' + now + ' (' + now + '/' + str(bot.get_contest_problem_num()) + ')')
            await message.channel.send('ソートなぞなぞ ソート前の文字列な〜んだ？\n' + bot.getProblem().problem)
        else:
            await message.channel.send('何らかの理由で問題の生成に失敗しました。')

# コンテストを開始する
async def run_contest(message):
    cmdlist = message.content.split(' ')
    if bot.contestRunning():
        response = 'コンテスト中です。コンテストの中止は -unrated で行えます。'
        await message.channel.send(response)
    elif bot.isGenerated():
        await message.channel.send('前回の出題が解かれていません\n問題: ' + bot.getProblem().problem)
    elif len(cmdlist) != 3:
        response = 'コンテストは \"-contest NUM \" の形式でのみ応答します'
        await message.channel.send(response)
    elif cmdlist[2] == 'NUM':
        response = 'NUM って言ったけどそうではなくて、NUM の部分には数字を入れて下さい'
        await message.channel.send(response)
    else:
        try:
            contest_problem_num = int(cmdlist[2])
            if contest_problem_num < 0:
                response = str(contest_problem_num) + '問のコンテストは出来ません…'
                await message.channel.send(response)
            else:
                if contest_problem_num > 70:
                    response = str(contest_problem_num) + '問はちょっと多くない？70問にしますね。'
                    await message.channel.send(response)
                    contest_problem_num = 70
                response = str(contest_problem_num) + '問のコンテストを始めます！'
                await message.channel.send(response)
                if bot.begin_contest(contest_problem_num):
                    await run_contest_problem(message)
                else:
                    await message.channel.send('何らかの理由でコンテストの開始に失敗しました。')

        except ValueError:
            response = 'コンテストは \"-contest NUM \" の形式でのみ応答します\n'
            response += 'NUM の部分には数字を入れて下さい'
            await message.channel.send(response)

# コンテストを開始する
async def run_unrated(message):
    response = 'コンテストを中断しました'
    await message.channel.send(response)
    bot.end_problem()
    bot.end_contest()

# 答えを判定する
async def check_answer(message):
    print('check answer : ' + message.content)
    if bot.checkAnswer(message.content, str(message.author)):
        win = bot.getWinnter()
        response = win[0] + ' さん、正解です！\n' + '正解は\"' + message.content + '\"でした！'
        await message.channel.send(response)
        bot.end_problem()
    elif bot.checkAnotherAnswer(message.content, str(message.author)):
        response = str(message.author) + ' さん、 \"' + message.content + '\" は非想定解ですが正解です！'
        await message.channel.send(response)

# 答えを判定する(コンテスト中)
async def check_contest_answer(message):
    print('check contest answer : ' + message.content)
    if bot.checkAnswer(message.content, str(message.author)):
        win = bot.getWinnter()
        response = win[0] + ' さん、正解です！\n' + '正解は\"' + message.content + '\"でした！'
        await message.channel.send(response)
        bot.end_contest_problem()
        print('contest running is : ' + str(bot.contestRunning()))
        if bot.has_next_contest_problem():
            await run_contest_problem(message)
        else:
            await message.channel.send(str(bot.get_contest_problem_num()) + '問連続の出題が終了しました。')
            bot.end_contest()
    elif bot.checkAnotherAnswer(message.content, str(message.author)):
        response = str(message.author) + ' さん、 \"' + message.content + '\" は非想定解ですが正解です！'
        await message.channel.send(response)

def getCmdList():
    return """
echo: -echo
出題: -prob
辞書の状態を見る: -dic-status
辞書を出題対象にする: -dic-select DIC_NAME
辞書を出題対象から外す: -dic-deselect DIC_NAME
問題のヒントを見る: -hint NUM
問題を諦める: -giveup
#連続で問題を出す: -contest NUM
#連続で問題を出すのを中止する: -unrated
困った時は: -reset
botを落とす(再起動は出来ません): -bye
"""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
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
            print('receive : ' + cmd)
            if cmd == '-echo':
                response = bot.echo(message.content)
                await message.channel.send(response)
            elif cmd == '-kick();':
                print('log : kick call')
                await message.channel.send('ヒィンｗ')
            elif cmd == '-bye':
                print('log : bye call')
                await run_quit(message)
            elif cmd == '-cmd':
                print('log : cmd call')
                response = getCmdList()
                await message.channel.send(response)
            elif cmd == '-reset':
                bot.reset()
                bot.selectAllDic()
                await message.channel.send('hard reset.')
            elif cmd == '-prob':
                print('log : prob call')
                if not bot.isGenerated():
                    if bot.generateProblem():
                        print(bot.getProblem())
                        await message.channel.send('ソートなぞなぞ ソート前の文字列な〜んだ？\n' + bot.getProblem().problem)
                    else:
                        await message.channel.send('何らかの理由で問題の生成に失敗しました。')
                else:
                    await message.channel.send('前回の出題が解かれていません\n問題: ' + bot.getProblem().problem)
            elif cmd == '-giveup':
                print('log : giveup call')
                if bot.isGenerated():
                    response = '正解は\"' + bot.getProblem().answer + '\"でした...'
                    await message.channel.send(response)
                    bot.endProblem()
                else:
                    response = '現在問題は出されていません'
                    await message.channel.send(response)
            elif cmd == '-dic-status':
                print('log : dic call')
                response = '現在の辞書の状態は以下です\n'
                state = bot.getAllDicStatus()
                for i in state:
                    response += '辞書名 : ' + i[0] + ' , 問題数 : ' + str(i[1]) + ' , 出題対象 : ' + str(i[2]) + '\n'
                await message.channel.send(response)
            elif cmd == '-hint':
                print('log : hint call')
                await run_hint(message)
            elif cmd == '-dic-select':
                print('log : select call')
                await run_select(message)
            elif cmd == '-dic-deselect':
                print('log : deselect call')
                await run_deselect(message)
            elif cmd == '-contest':
                print('log : cotest call')
                await run_contest(message)
            elif cmd == '-unrated':
                print('log : unrated call')
                await run_unrated(message)
            elif cmd[0] == '-':
                print('log : -XXX command call')
                print(cmd[1:len(cmd)])
                if cmd[1:len(cmd)] in bot.getDicNameList():
                    if not bot.isGenerated():
                        if bot.generateProblemWithSelect(cmd[1:len(cmd)]):
                            print(bot.getProblem())
                            await message.channel.send('ソートなぞなぞ ソート前の文字列な〜んだ？\n' + bot.getProblem().problem)
                        else:
                            await message.channel.send('何らかの理由で問題の生成に失敗しました。')
                    else:
                        await message.channel.send('前回の出題が解かれていません\n問題: ' + bot.getProblem().problem)
                else:
                    await message.channel.send(cmd + ' コマンドは未定義です。')

    elif bot.isGenerated(): # 答えの確認
        print('check answer : ' + message.content)
        if bot.contestRunning():
            await check_contest_answer(message)
        else:
            await check_answer(message)

    lock.release()

client.run(token)
