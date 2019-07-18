#!/usr/bin/python3
import urllib.request
import re
import time
from pyquery import PyQuery as pq

def solve(url):

    # 文字の長さ
    DATA_LENGTH=8

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20110101 Firefox/47.0"}

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')

    data = pq(html, parser='html')

    # ひらがな、かたかなのみで構成される8文字かどうかの確認
    re_checker = re.compile(r'[あ-んア-ン]{8}$')

    for x in data.find('p'):
        texts = pq(x).text().split()
        for item in texts:
            if re_checker.fullmatch(item):
                print(item, ''.join(sorted(item)))

# もじぴったん 8文字の言葉 あ〜お
solve('https://wikiwiki.jp/mojids/8-a')

solve('https://wikiwiki.jp/mojids/8ka')

solve('https://wikiwiki.jp/mojids/8si')

solve('https://wikiwiki.jp/mojids/8ha')

