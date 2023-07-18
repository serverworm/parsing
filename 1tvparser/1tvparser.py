import requests
import asyncio
from random import randrange
from lxml import html
import logging
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def random_headers(rand):
    if rand == False:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
    else:
        headers = {
            'User-Agent': f'Mozilla/{randrange(0, 50) / 10} (Macintosh; Intel Mac OS X {randrange(0, 9)}_{randrange(0, 9)}) AppleWebKit/{randrange(0, 999)}.{randrange(0, 99)} '
                          f'(KHTML, like Gecko) Chrome/{randrange(0, 99)}.{randrange(0, 9)}.{randrange(0, 9999)}.{randrange(0, 999)} Safari/{randrange(0, 999)}.{randrange(0, 99)}'
        }
    return headers


async def get_last_new(url, count):
    logging.info(f'URL new: {url}')
    try:
        second_response = requests.get(url, headers=random_headers(True))
        second_tree = html.document_fromstring(second_response.text)
    except Exception as ex:
        logging.error('ERROR IN SECOND RESPONSE: ', ex)

    try:
        header_last_new = second_tree.xpath('/html/body/main/div[5]/div[2]/div/div[1]/article/div[1]/header/h1/text()')
        header_last_new = ''.join(header_last_new)
        logging.info(header_last_new)
    except Exception as ex:
        logging.error('ERROR IN header_last_new: ', ex)

    try:
        caption_last_new = second_tree.xpath(
            '/html/body/main/div[5]/div[2]/div/div[1]/article/div[4]/div/div/div/div/div/p/text()')
        caption_last_new = '📰 В этом выпуске: \n' + ''.join(caption_last_new).capitalize()
        logging.info(caption_last_new)
    except Exception as ex:
        logging.error('ERROR IN caption_last_new: ', ex)

    return count + 1


async def main():
    count = 457264
    url = 'https://www.1tv.ru/n/' + str(count)
    while True:
        await get_last_new(url, count)
        count += 1
        time.sleep(50000)


if __name__ == "__main__":
    asyncio.run(main())
