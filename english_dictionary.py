#!/usr/bin/python3
import urllib.request
import re
import time
from pyquery import PyQuery as pq

def solve(url):

    # 文字の長さ
    DATA_LENGTH=5

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20110101 Firefox/47.0"}

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('shift-JIS')

    data = pq(html, parser='html')

    # ひらがな、かたかなのみで構成される5文字以上かどうかの確認
    re_checker = re.compile(r'[a-z]{5}[a-z]*$')

    for x in data.find('td'):
        texts = pq(x).text().split()
        if len(texts) == 1:
            item = texts[0]
            if re_checker.fullmatch(item):
                sorted_item = ''.join(sorted(item))
                if sorted_item != item:
                    print(item, sorted_item)


# 英語漬け.com TOEIC頻出1~300
solve('http://www.eigo-duke.com/tango/TOEIC1-300.html')

# 英語漬け.com TOEIC頻出301~600
solve('http://www.eigo-duke.com/tango/TOEIC301-600.html')

# 英語漬け.com TOEIC頻出601~900
solve('http://www.eigo-duke.com/tango/TOEIC601-900.html')

# 英語漬け.com TOEIC頻出901~1200
solve('http://www.eigo-duke.com/tango/TOEIC901-1200.html')

# 英語漬け.com TOEIC頻出1201~1500
solve('http://www.eigo-duke.com/tango/TOEIC1201-1500.html')
