import asyncio
import os
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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


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


def checking_for_a_new_video(tree):
    name_last_video = ''.join(tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[2]/h1/text()'))
    if name_last_video == f'Видео {countlastvideo} находится в процессе подготовки!':
        return False
    else:
        return True


def name_last_video(tree, countlastvideo):
    try:
        name_last_video = ''.join(tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[2]/h1/text()'))
        logging.info(name_last_video)
        return name_last_video
    except Exception as ex:
        logging.error('ERROR in name_last_video: ', ex)


def tags_last_video(tree):
    try:
        tags_last_video = []
        i = 1
        while tree.xpath(
                f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{i}]/text()') != tree.xpath(
            f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{999}]/text()'):
            tags_last_video.append(*tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{i}]/text()'))
            i += 1
        for i in range(len(tags_last_video)):
            tags_last_video[i] = tags_last_video[i].replace(' ', '')
        urltags = ' '.join(tags_last_video)
        logging.info(urltags)
        return urltags
    except Exception as ex:
        logging.error('ERROR in tags_last_video: ', ex)


def get_preview_last_video(response):
    try:
        get_preview_last_video = []
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('script')
        i = 1
        for link in links:
            if "image: '" in str(link):
                get_preview_last_video += [str(link).split("'")[x] for x in range(len(str(link).split("'"))) if
                                           'jpg' in str(link).split("'")[x]]
        get_preview_last_video = ''.join(get_preview_last_video)
        return get_preview_last_video
    except Exception as ex:
        logging.error('ERROR in get_preview_last_video: ', ex)


def get_content_last_video(response):
    try:
        get_content_last_video = []
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            if 'HD качестве' in str(link):
                href = link.get('href')
                if href:
                    if '.mp4' in str(href):
                        get_content_last_video = str(
                            href) + f'&amp;file=mob.porno365.bond_{countlastvideo}_hd.mp4&amp;downloading'
        return get_content_last_video
    except Exception as ex:
        logging.error('ERROR in urldownloadvideo: ', ex)


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

        try:
            with open(file_path, "wb") as file:
                file.write(response.content)
        except Exception as ex:
            logging.error('ERROR during photo upload: ', ex)


def download_video(urldownloadvideo, folder_path):
    # Загрузка видео по ссылке
    file_path = os.path.join('videos', f'{countlastvideo}.mp4')
    if os.path.isfile(file_path):
        logging.info(f"Файл {countlastvideo}.mp4 уже в папке videos")
    else:
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


async def send_to_chanel(namelastvideo, urltags):
    combined_symbols = choice(['❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '💗', '💓']) + choice(
        ['😏', '😈', '🍆', '🍑', '🙈', '🙊', '🍌', '🍒', '🌶️', '👅', '🤤', '😋', '😍', '😘', '🥰', '🤩', '🤗', '🥵', '🤪', '🤭', '🧐', '😻',
         '😽', '😼', '👀'])
    logging.info(f'Выгружаю видео {countlastvideo}.mp4 и фото {countlastvideo}.jpg на канал...')
    try:
        with open(f'videos/{countlastvideo}.mp4', 'rb') as f:
            with open(f'videos/{countlastvideo}.jpg', 'rb') as f1:
                await client.send_file(-1001533404742, file=f1,
                                       caption=f'{combined_symbols} {namelastvideo}\n\n{urltags}')
                await client.send_file(-1001533404742, file=f,
                                       caption=f'[👉 PORNO365, ПОДПИШИСЬ!](https://t.me/+gFS3rVOCtfM0Zjdi)',
                                       attributes=(DocumentAttributeVideo(183, 1280, 720),), supports_streaming=True,
                                       part_size_kb=1024)
        logging.info(f'Видео {countlastvideo}.mp4  и фото {countlastvideo}.jpg выгруженно на канал.')
    except Exception as ex:
        logging.error('ERROR in send to chanel: ', ex)


def delete_past_content():
    try:
        files_to_delete = [f'videos/{countlastvideo}.jpg', f'videos/{countlastvideo}.mp4']
        for file_name in files_to_delete:
            file_path = os.path.join(file_name)  # Составляем полный путь к файлу
            if os.path.exists(file_path):  # Проверяем, существует ли файл
                os.remove(file_path)  # Удаляем файл
        logging.info("Видео {countlastvideo}.mp4  и фото {countlastvideo}.jpg успешно удалены.\n\n")
    except Exception as ex:
        logging.error('ERROR in files_to_delete: ', ex)


async def main(actual_url, countlastvideo, awit=None):
    logging.info('The bot has started working.')
    try:
        await client.start()
    except Exception as ex:
        logging.error('ERROR in client.start(): ', ex)
    while True:
        url = actual_url + "/movie/" + str(countlastvideo)
        try:
            response = requests.get(url, headers=random_headers(True, url))
            tree = html.document_fromstring(response.text)
        except Exception as ex:
            logging.error('ERROR in response: ', ex)
        if name_last_video(tree, countlastvideo) != f'Видео {countlastvideo} находится в процессе подготовки!':
            logging.info('Starting to prepare the post...')
            download_photo(get_preview_last_video(response), 'videos')
            download_video(get_content_last_video(response), 'videos')
            await send_to_chanel(name_last_video(tree, countlastvideo), tags_last_video(tree))
            delete_past_content()
            countlastvideo += 1
        time.sleep(180)


if __name__ == "__main__":
    countlastvideo = 36543
    actual_url = "http://mob.porno365.bond/"
    asyncio.run(main(actual_url, countlastvideo))
