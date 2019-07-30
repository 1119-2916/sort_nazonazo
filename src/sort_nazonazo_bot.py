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
        self.__answers = None
        self.__winner = []
        self.__anotherWinner = []
        self.__contestCount = 0
        self.__contestProblemNum = 0
        self.__contestProblems = None

    def echo(self, cmd):
        return cmd

    # 指定した名前で管理される辞書の単語数を取得
    def getDicSize(self, dic:str):
        tmp = list(filter(lambda x:x.getCmd() == dic, self.__dictionaries))
        if len(tmp) <= 0:
            return -1
        else:
            return tmp[0].getSize()

    # 辞書選択の状態を変更 辞書は状態として複数選択が可能
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

    # 現在出題している問題を取得 ない場合は None
    def getProblem(self) -> Nazonazo:
        return self.__nazonazo;

    # 問題生成 辞書から問題を1問選んでbotを出題状態にする
    def generateProblem(self):
        print('log : call generate Problem')
        if self.__nazonazo is not None:
            print('log WARN : problem is selected')
            return False
        dic = [] # 選択されている辞書を連結する
        for i in self.__dictionaries:
            if i.isSelected():
                dic.extend(i.getDictionary())
                print('log : append ' + i.getCmd())
        if len(dic) == 0:
            print('log WARN : dic not found. failed to fetch nazonazo')
            return False
        self.__nazonazo = dic[random.randrange(len(dic))]
        self.__answers = set()
        for i in dic:
            self.__answers.add(i.answer)
        return True

    # 辞書を選択して出題する
    def generateProblemWithSelect(self, dic_name:str):
        print('log : call generate Problem with select ' + dic_name)
        if self.__nazonazo is not None:
            print('log WARN : problem is selected')
            return False
        dic = [] # 選択されている辞書を連結する
        for i in self.__dictionaries:
            if i.getCmd() == dic_name:
                dic.extend(i.getDictionary())
        if len(dic) == 0:
            print('log WARN : dic not found. failed to fetch nazonazo')
            return False
        self.__nazonazo = dic[random.randrange(len(dic))]
        self.__answers = set()
        for i in dic:
            self.__answers.add(i.answer)
        return True

    # 問題が生成されている状態かどうかを返す
    def isGenerated(self):
        return self.__nazonazo is not None

    # 受け取った答えが想定解か判定する
    def checkAnswer(self, ans:str, user:str = None) -> bool:
        if self.__nazonazo is None:
            print('log WARN : problem is not generated')
            return False
        if ans == self.__nazonazo.answer:
            self.__winner.append(user)
            return True
        else:
            return False

    # 受け取った答えが非想定解か判定する
    def checkAnotherAnswer(self, ans:str, user:str = None) -> bool:
        if self.__nazonazo is None:
            print('log WARN : problem is not generated')
            return False
        if sorted(ans) == sorted(self.__nazonazo.answer) and ans != self.__nazonazo.answer and ans in self.__answers:
            self.__anotherWinner.append([ans, user])
            return True

    # 現在の正解者リストを取得
    def getWinnter(self):
        return self.__winner

    # 現在の非想定解正解者リストを取得
    def getAnotherWinner(self):
        return self.__anotherWinner
    
    # 問題を出題していない状態にする
    def end_problem(self):
        self.__nazonazo = None
        self.__answers = None
        self.__anotherWinner = None

    # コンテストを開始するために設定をする 設定の成功失敗を返す
    def begin_contest(self, num:int):
        print('log : call begin contest ' + str(num))
        if self.__nazonazo is not None:
            print('log WARN : problem is selected')
            return False
        if self.__contestCount != 0:
            print('log WARN : contest is running')
            return False
        self.__contestCount = num
        self.__contestProblemNum = num
        dic = [] # 選択されている辞書を連結する
        for i in self.__dictionaries:
            if i.isSelected():
                dic.extend(i.getDictionary())
                print('log : append ' + i.getCmd())
        if len(dic) == 0:
            print('log WARN : dic not found. failed to fetch nazonazo')
            return False
        self.__contestProblems = dic
        self.__answers = set()
        for i in dic:
            self.__answers.add(i.answer)
        return True

    def get_contest_problem_num(self):
        return self.__contestProblemNum

    def get_contest_problem_count(self):
        return self.__contestCount

    # コンテスト中かどうかを返す
    def contestRunning(self):
        return self.__contestProblemNum != 0

    # コンテスト中かどうかを返す
    def has_next_contest_problem(self):
        return self.__contestCount != 0
    
    # コンテスト中なら次の問題を出す
    def generateContestProblem(self):
        print('log : call next problem in contest ' + str(self.__contestCount))
        if self.__nazonazo is not None:
            print('log WARN : problem is selected')
            return False
        if self.__contestProblemNum == 0 or self.__contestCount == 0:
            print('log WARN : contest is not running')
            return False
        self.__nazonazo = self.__contestProblems[random.randrange(len(self.__contestProblems))]
        return True

    # コンテスト中なら問題の後処理をする
    def end_contest_problem(self):
        print('log : call clear problem in contest ' + str(self.__contestCount))
        if self.__nazonazo is None:
            print('log WARN : problem is not selected')
            return False
        if self.__contestProblemNum == 0:
            print('log WARN : contest is not running')
            return False
        self.end_problem()
        self.__contestCount -= 1;
        return True

    # コンテストの後処理
    def end_contest(self):
        self.__contestCount = 0
        self.__contestProblemNum = 0
        self.__contestProblems = None

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

