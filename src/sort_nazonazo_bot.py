import sys
import random
from typing import List

class Nazonazo:

    def __init__(self, ans:str, prob:str):
        self.__answer = ans
        self.__problem = prob

    def __repr__(self):
        return "['%s', '%s']" % (self.answer, self.problem)

    @property
    def problem(self):
        return self.__problem

    @property
    def answer(self):
        return self.__answer

NazonazoList = List[Nazonazo]

class NazonazoDictionary:

    # 辞書となるリストとコマンド名を要求する
    def __init__(self, dictionary:NazonazoList, cmd:str):
        # 改行除去は本来ここでするべきではない
        self.__cmd = cmd.replace('\n', '')
        self.__dictionary = dictionary
        self.__size = len(dictionary)
        self.__selected = True

    def getSize(self):
        return self.__size

    def getCmd(self):
        return self.__cmd

    def getDictionary(self):
        return self.__dictionary

    def isSelected(self):
        return self.__selected

    def select(self):
        self.__selected = True

    def cancel(self):
        self.__selected = False

    # 辞書選択の状態を変更
    def setSelected(self, status:bool):
        self.__selected = status

    def getStatus(self):
        return [self.__cmd, self.__size, self.__selected]

NazonazoDictionaries = List[NazonazoDictionary]

class SortNazonazoBot:
    # private status
    #__question_solving = False
    #__contest_solving = False
    #__contest_problem_num = 0;
    #__contest_solving_num = 0;

    # NazonazoDictionaryのリストを要求する
    def __init__(self, dictionaries:NazonazoDictionaries = []):
        self.__dictionaries = dictionaries
        print('dictionary size :' , len(dictionaries))
        if len(dictionaries) == 0:
            print('dictionary not found')
        self.reset()

    # 指定したファイルパスからファイルを読んで辞書を読み込む
    def readDictionaries(self, filePath:str):
        try:
            dictionary_list_file = open(filePath, 'r')
            dictionaries:List[NazonazoDictionary] = []
            for dictionary_file_name in dictionary_list_file:
                print(dictionary_file_name.replace('\n',''), end='')
                info = dictionary_file_name.split(' ')
                if len(info) != 2:
                    print('invalid file format.')
                    continue
                try:
                    dictionary_file = open(info[0], 'r')
                    dic:NazonazoList = []
                    for sentence in dictionary_file:
                        tmp = sentence.replace('\n','').split(' ')
                        dic.append(Nazonazo(tmp[0], tmp[1]))
                    dictionaries.append(NazonazoDictionary(dic, info[1].replace('\n', '')))
                    print(' size : ' + str(len(dic)))
                except:
                    print('file could not read')
            self.__dictionaries = dictionaries
        except:
            print('failed to find or read dictionary list file. check your dictionary list file')
            
    def reset(self):
        self.__nazonazo = None

    def echo(self, cmd):
        return cmd

    def getCmdList(self):
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

    # 指定した名前で管理される辞書の単語数を取得
    def getDicSize(self, dic:str):
        tmp = list(filter(lambda x:x.getCmd() == dic, self.__dictionaries))
        if len(tmp) <= 0:
            return -1
        else:
            return tmp[0].getSize()

    # 辞書選択の状態を変更 複数選択が可能
    def setDicSelected(self, dic:str, status:bool):
        tmp = list(filter(lambda x:x.getCmd() == dic, self.__dictionaries))
        if len(tmp) <= 0:
            print('log: ' + dic + ' not found.')
        else:
            print('log: set ' + dic + '(' + str(tmp[0].isSelected()) + ') to ' + str(status))
            tmp[0].setSelected(status)

    # 辞書選択の状態を変更 複数選択が可能
    def resetDicSelected(self):
        print('log: reset all dic FALSE')
        for i in self.__dictionaries:
            i.cancel()

    # 辞書選択の状態を変更 複数選択が可能
    def selectAllDic(self):
        print('log: set all dic TRUE')
        for i in self.__dictionaries:
            i.select()

    # 保持する全ての辞書の名前をリストで取得
    def getDicNameList(self):
        return list(map(lambda x:x.getCmd(), self.__dictionaries))

    # 保持する全ての辞書の名前と登録単語数をリストで取得
    def getAllDicStatus(self):
        return list(map(lambda x:x.getStatus(), self.__dictionaries))

    # 選択されている辞書から問題を1問取ってくる ない場合は空のリストを返す
    def selectProblem(self) -> Nazonazo:
        print('log : call get Problem')
        dic = []
        for i in self.__dictionaries:
            if i.isSelected():
                dic.extend(i.getDictionary())
                print('log : append ' + i.getCmd())
        if len(dic) == 0:
            print('log WARN : dic not found')
            return None
        return dic[random.randrange(len(dic))]

    # 現在出題している問題を取得 ない場合は None
    def getProblem(self) -> Nazonazo:
        return self.__nazonazo;

    # 問題生成 辞書から問題を1問選んでbotを出題状態にする
    def generateProblem(self):
        if self.__nazonazo is not None:
            print('log WARN : problem is selected')
            return False
        prob:nazonazo = self.selectProblem()
        if prob is None:
            print('log WARN : faild to fetch nazonazo')
            return False
        self.__nazonazo = prob
        return True

    # 問題が生成されている状態かどうかを返す
    def isGenerated(self):
        return self.__nazonazo is not None

    # 受け取った答えが正当か判定する
    def sendAnswer(self, ans:str) -> bool:
        if self.__nazonazo is None:
            print('log WARN : problem is not generated')
            return False
        return ans == self.__nazonazo.answer
    
    # 問題を出題していない状態にする
    def clearProblem(self):
        self.__nazonazo = None

def test(src):
    try:
        dictionary_list_file = open(src, 'r')
        dictionaries:List[NazonazoDictionary] = []
        for dictionary_file_name in dictionary_list_file:
            print(dictionary_file_name.replace('\n',''), end='')
            info = dictionary_file_name.split(' ')
            if len(info) != 2:
                print('invalid file format.')
                continue
            try:
                dictionary_file = open(info[0], 'r')
                dic:NazonazoList = []
                for sentence in dictionary_file:
                    #print(type(sentence.replace('\n','').split(' ')))
                    #dic.append(sentence.replace('\n','').split(' '))
                    tmp = sentence.replace('\n','').split(' ')
                    dic.append(Nazonazo(tmp[0], tmp[1]))
                dictionaries.append(NazonazoDictionary(dic, info[1].replace('\n', '')))
                print(' size : ' + str(len(dic)))
            except:
                print('file could not read')
        return SortNazonazoBot(dictionaries)
    except:
        print('failed to find or read dictionary list file. check your dictionary list file')
        sys.exit()
""" bot = test('dictionary_list')
print(bot.getAllDicStatus())
print(bot.getDicNameList())
bot.setDicSelected(bot.getDicNameList()[0], False)
print(bot.getAllDicStatus())
bot.setDicSelected(bot.getDicNameList()[0], True)
bot.resetDicSelected()
print(bot.getAllDicStatus())
bot.selectAllDic()
print(str(bot.getAllDicStatus()) + 'bot.getAllDicStatus()')
print(str(bot.generateProblem()) + 'bot.generateProblem()')
print(str(bot.isGenerated()) + 'bot.isGenerated()')
print(str(bot.getProblem()) + 'bot.getProblem()')
print(str(bot.generateProblem()) + 'bot.generateProblem()')
print(str(bot.isGenerated()) + 'bot.isGenerated()')
print(str(bot.sendAnswer("hohoho")) + 'bot.sendAnswer("hohoho")')
print(str(bot.clearProblem()) + 'bot.clearProblem()')
print(str(bot.isGenerated()) + 'bot.isGenerated()')
"""
