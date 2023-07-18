from random import randrange
import requests
from bs4 import BeautifulSoup
from lxml import html
import re

url = 'https://rt.pornhub.com/view_video.php?viewkey=643d1a6e1332e'

def random_headers(rand, url):
    if rand == False:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Referer': url
        }
    else:
        headers = {
            'User-Agent': f'Mozilla/{randrange(0, 50) / 10} (Macintosh; Intel Mac OS X {randrange(0, 9)}_{randrange(0, 9)}) AppleWebKit/{randrange(0, 999)}.{randrange(0, 99)} '
                          f'(KHTML, like Gecko) Chrome/{randrange(0, 99)}.{randrange(0, 9)}.{randrange(0, 9999)}.{randrange(0, 999)} Safari/{randrange(0, 999)}.{randrange(0, 99)}',
            'Referer': url
        }
    return headers

response = requests.get(url, headers=random_headers(True, url))
tree = html.document_fromstring(response.text)

tag = 1
tags_video = []
while tree.xpath(f'//*[@id="hd-leftColVideoPage"]/div[1]/div[6]/div[1]/div[4]/div[2]/div[2]/div[1]/a[{tag}]/text()') != []:
    tags_video.append('#' + ''.join(tree.xpath(f'//*[@id="hd-leftColVideoPage"]/div[1]/div[6]/div[1]/div[4]/div[2]/div[2]/div[1]/a[{tag}]/text()')).replace(' ', ''))
    tag += 1
tags_video = ' '.join(tags_video)
print(tags_video)
