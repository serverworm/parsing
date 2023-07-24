import sys

import requests
import asyncio
from random import randrange
from lxml import html
import logging
import time
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

api_id = 
api_hash = ''

client = TelegramClient('my_session', api_id, api_hash,
                        device_model="iPhone 13 Pro Max",
                        system_version="14.8.1",
                        app_version="8.4",
                        lang_code="en",
                        system_lang_code="en-US")

# try:
#     client.disconnect()
# except Exception as ex:
#     logging.error('ERROR in client.disconnect(): ', ex)


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


def download_video(urldownloadvideo, folder_path):
    # Загрузка видео по ссылке
    file_path = os.path.join('videos', f'{countlastvideo}.mp4')
    if os.path.isfile(file_path):
        logging.info(f"Файл {countlastvideo}.mp4 уже в папке videos")
    else:
        logging.info("Видео загружается...")
        file_name = f'{countlastvideo}.mp4'
        file_path = os.path.join(folder_path, file_name)
        try:
            response = requests.get(urldownloadvideo)
        except Exception as ex:
            logging.error('ERROR in response in download_video func: ', ex)
        try:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    file.write(chunk)
        except Exception as ex:
            logging.error('ERROR during video upload: ', ex)
        logging.info("Видео загружено.")



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

    try:
        href_on_downloading_video = second_tree.xpath('')

    # download_video('https://www.1tv.ru/n/' + str(count), 'videonews')
    try:
        await client.start()
    except Exception as ex:
        logging.info('ERROR in client.start(): ', ex)

    with open('videonews/file.mp4', 'rb') as f:
        logging.info('Upload the news to the channel...')
        await client.send_file(-1001852228260, file=f,
                               caption=f'🆕 {header_last_new}\n\n{caption_last_new}',
                               attributes=(DocumentAttributeVideo(0, 0, 0),), supports_streaming=True)
        logging.info('News on the channel.')

    try:
        await client.disconnect()
    except Exception as ex:
        logging.error('ERROR in client.disconnect(): ', ex)

    return count + 1


# https://v2-dtln.1internet.tv/video/multibitrate/video/2023/07/18/ccb7606f-cd88-48b5-ab8a-05b1335bcab2_HD-news-2023_07_18-13_16_30_,350,950,3800,.mp4.urlset/seg-3-f2-v1-a1.ts
# https://v2-dtln.1internet.tv/video/multibitrate/video/2023/07/18/ccb7606f-cd88-48b5-ab8a-05b1335bcab2_HD-news-2023_07_18-13_16_30_,350,950,3800,.mp4.urlset/seg-2-f2-v1-a1.ts
# https://v2-dtln.1internet.tv/video/multibitrate/video/2023/07/18/ccb7606f-cd88-48b5-ab8a-05b1335bcab2_HD-news-2023_07_18-13_16_30_,350,950,3800,.mp4.urlset/seg-1-f2-v1-a1.ts
# https://v2-dtln.1internet.tv/video/multibitrate/video/2023/07/18/202535f7-4d0d-4bf2-96f1-44edff35eda8_HD-news-2023_07_18-13_18_58_,350,950,3800,.mp4.urlset/seg-1-f1-v1-a1.ts
async def main():
    count = 457339
    while True:
        url = 'https://www.1tv.ru/n/' + str(count)
        await get_last_new(url, count)
        count += 1
        time.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())

