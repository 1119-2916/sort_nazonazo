#!/usr/bin/python3
import urllib.request
import re
import time
from pyquery import PyQuery as pq

def solve(url):

    # 文字の長さ
    DATA_LENGTH=9

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20110101 Firefox/47.0"}

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')

    data = pq(html, parser='html')

    # ひらがな、かたかなのみで構成される9文字かどうかの確認
    re_checker = re.compile(r'[あ-んア-ン]{9}$')

    for x in data.find('p'):
        texts = pq(x).text().split()
        for item in texts:
            if re_checker.fullmatch(item):
                print(item, ''.join(sorted(item)))

# もじぴったん 8文字の言葉 あ〜お
#solve('https://wikiwiki.jp/mojids/8-a')

#solve('https://wikiwiki.jp/mojids/8ka')

#solve('https://wikiwiki.jp/mojids/8si')

#solve('https://wikiwiki.jp/mojids/8ha')

# もじぴったん 9文字の言葉
solve('https://wikiwiki.jp/mojids/%EF%BC%99%E6%96%87%E5%AD%97%E3%81%AE%E8%A8%80%E8%91%89')

solve('https://wikiwiki.jp/mojids/%EF%BC%99%E6%96%87%E5%AD%97%E3%81%AE%E8%A8%80%E8%91%89%EF%BC%88%EF%BC%92%EF%BC%89%E3%81%99%EF%BD%9E%E3%82%8F')
