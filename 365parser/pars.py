import asyncio
import os
import sys
import logging
from bs4 import BeautifulSoup
import requests
import time
from lxml import html
from random import randrange, choice
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo

api_id = 12064443
api_hash = '608f11694b2ba722a53561faa7f3444f'

client = TelegramClient('my_session', api_id, api_hash,
                        device_model="iPhone 13 Pro Max",
                        system_version="14.8.1",
                        app_version="8.4",
                        lang_code="en",
                        system_lang_code="en-US")
try:
    client.disconnect()
except Exception as ex:
    logging.info('ERROR in client.disconnect(): ', ex)

url = "http://mob.porno365.bond/"
countlastvideo = 36427


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
logging.info('Начало работы Бота.')

def random_headers(rand):
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


def download_photo(urldownloadphoto, folder_path):
    file_path = os.path.join('videos', f'{countlastvideo}.jpg')
    if os.path.isfile(file_path):
        logging.info(f"Файл {countlastvideo}.jpg уже в папке videos")
    else:
        file_name = f'{countlastvideo}.jpg'
        file_path = os.path.join(folder_path, file_name)
        try:
            response = requests.get(urldownloadphoto)
        except Exception as ex:
            logging.error('ERROR in response in download_photo func: ', ex)

        logging.info("Фото загружается...")
        try:
            with open(file_path, "wb") as file:
                file.write(response.content)
        except Exception as ex:
            logging.error('ERROR during photo upload: ', ex)
        logging.info("Фото загружено.")


async def getnewvideo(url, countlastvideo):
    try:
        response = requests.get(url, headers=random_headers(True))
        tree = html.document_fromstring(response.text)
    except Exception as ex:
        logging.error('ERROR in first response in getnewvideo func: ', ex)

    try:
        namelastvideo = ''.join(tree.xpath(f'//*[@id="{countlastvideo}"]/a/p/text()'))
        logging.info(namelastvideo)
    except Exception as ex:
        logging.error('ERROR in namelastvideo: ', ex)

    try:
        urllastvideo = str(tree.xpath(f'//*[@id="{countlastvideo}"]/a/@href')[0])
        logging.info(urllastvideo)
    except Exception as ex:
        logging.error('ERROR in urllastvideo: ', ex)

    try:
        second_response = requests.get(f'{url}/movie/{countlastvideo}', headers=random_headers(True))
        second_tree = html.document_fromstring(second_response.text)
    except Exception as ex:
        logging.error('ERROR in second response in getnewvideo func: ', ex)

    try:
        urltags = []
        i = 1
        while second_tree.xpath(
                f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{i}]/text()') != second_tree.xpath(
            f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{999}]/text()'):
            urltags.append(*second_tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{i}]/text()'))
            i += 1

        for i in range(len(urltags)):
            urltags[i] = urltags[i].replace(' ', '')
        urltags = ' '.join(urltags)
        logging.info(urltags)
    except Exception as ex:
        logging.error('ERROR in urltags: ', ex)

    try:
        urldownloadvideo = []
        soup = BeautifulSoup(second_response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            if 'HD качестве' in str(link):
                href = link.get('href')
                if href:
                    if '.mp4' in str(href):
                        urldownloadvideo = str(
                            href) + f'&amp;file=mob.porno365.bond_{countlastvideo}_hd.mp4&amp;downloading'

        logging.info(urldownloadvideo)
    except Exception as ex:
        logging.error('ERROR in urldownloadvideo: ', ex)

    try:
        urldownloadphoto = []
        soup = BeautifulSoup(second_response.text, 'html.parser')
        links = soup.find_all('script')
        i = 1
        for link in links:
            if "image: '" in str(link):
                urldownloadphoto += [str(link).split("'")[x] for x in range(len(str(link).split("'"))) if
                                     'jpg' in str(link).split("'")[x]]
        urldownloadphoto = ''.join(urldownloadphoto)
        logging.info(urldownloadphoto)
    except Exception as ex:
        logging.error('ERROR in urldownloadphoto: ', ex)
    sys.exit()
    # Загрузка фото и видео по ссылке
    download_photo(urldownloadphoto, 'videos')
    download_video(urldownloadvideo, 'videos')

    combined_symbols = choice(['❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '💗', '💓']) + choice(
        ['😏', '😈', '🍆', '🍑', '🙈', '🙊', '🍌', '🍒', '🌶️', '👅', '🤤', '😋', '😍', '😘', '🥰', '🤩', '🤗', '🥵', '🤪', '🤭', '🧐', '😻', '😽', '😼', '👀'])
    logging.info(f'Выгружаю видео {countlastvideo}.mp4 и фото {countlastvideo}.jpg на канал...')
    try:
        await client.start()
    except Exception as ex:
        logging.error('ERROR in client.start(): ', ex)
    try:
        with open(f'videos/{countlastvideo}.mp4', 'rb') as f:
            with open(f'videos/{countlastvideo}.mp4', 'rb') as f1:
                await client.send_file(-1001533404742, file=[f1, f],
                                       caption=f'{combined_symbols} {namelastvideo}\n\n{urltags}\n\n[👉 PORNO365, ПОДПИШИСЬ!](https://t.me/+gFS3rVOCtfM0Zjdi)',
                                       attributes=(DocumentAttributeVideo(0, 0, 0),), supports_streaming=True)
        logging.info(f'Видео {countlastvideo}.mp4  и фото {countlastvideo}.jpg выгруженно на канал.')
    except Exception as ex:
        logging.error('ERROR in send to chanel: ', ex)

    try:
        await client.disconnect()
    except Exception as ex:
        logging.error('ERROR in client.disconnect(): ', ex)

    try:
        files_to_delete = [f'videos/{countlastvideo}.jpg', f'videos/{countlastvideo}.mp4']
        for file_name in files_to_delete:
            file_path = os.path.join(file_name)  # Составляем полный путь к файлу
            if os.path.exists(file_path):  # Проверяем, существует ли файл
                os.remove(file_path)  # Удаляем файл

        logging.info("Видео {countlastvideo}.mp4  и фото {countlastvideo}.jpg успешно удалены.\n\n")

    except Exception as ex:
        logging.error('ERROR in files_to_delete: ', ex)

async def main(url, countlastvideo):
    while True:
        await getnewvideo(url, countlastvideo)
        countlastvideo += 1
        time.sleep(1200)


if __name__ == "__main__":
    asyncio.run(main(url, countlastvideo))
