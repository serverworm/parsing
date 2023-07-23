import os
import time
import logging
import asyncio
import requests
from lxml import html
from bs4 import BeautifulSoup
from telethon import TelegramClient
from random import randrange, choice
from telethon.tl.types import DocumentAttributeVideo

# get on https://my.telegram.org/auth
api_id = 12064443
api_hash = '608f11694b2ba722a53561faa7f3444f'

# device configurator for creating a session, DO NOT LOG IN TO YOUR ACCOUNT WITHOUT USING IT!
client = TelegramClient('my_session', api_id, api_hash,
                        device_model="iPhone 13 Pro Max",
                        system_version="14.8.1",
                        app_version="8.4",
                        lang_code="en",
                        system_lang_code="en-US")
# configuring the bot logging level
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# a function for creating a unique User-Agent to bypass blocking requests to the server
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


# function for getting the title of the last video
def title_of_the_last_video(tree):
    try:
        title_of_the_last_video = ''.join(tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[2]/h1/text()'))
        logging.info(title_of_the_last_video)
        return title_of_the_last_video
    except Exception as ex:
        logging.error('ERROR in title_of_the_last_video: ', ex)


# function for getting video description
def get_a_description_for_the_video(tree):
    try:
        get_a_description_for_the_video = []
        i = 1

        while tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[9]/text()[{i}]') != []:
            get_a_description_for_the_video.append(
                ''.join(
                    tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[9]/text()[{i}]')) + '`' + ''.join(
                    tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[9]/span[{i}]/text()')) + '`')
            i += 1
        get_a_description_for_the_video = ''.join(get_a_description_for_the_video)[:-2]
        return get_a_description_for_the_video
    except Exception as ex:
        logging.error('ERROR in get_a_description_for_the_video: ', ex)


# function for getting video tags
def getting_the_tags_of_the_last_video(tree):
    try:
        getting_the_tags_of_the_last_video = []
        i = 1
        while tree.xpath(
                f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{i}]/text()') != tree.xpath(
            f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{999}]/text()'):
            getting_the_tags_of_the_last_video.append(
                *tree.xpath(f'//*[@id="content"]/div[1]/div[1]/div[1]/div[3]/div[10]/a[{i}]/text()'))
            i += 1
        for i in range(len(getting_the_tags_of_the_last_video)):
            getting_the_tags_of_the_last_video[i] = getting_the_tags_of_the_last_video[i].replace(' ', '')
        urltags = ' '.join(getting_the_tags_of_the_last_video)
        logging.info(urltags)
        return urltags
    except Exception as ex:
        logging.error('ERROR in getting_the_tags_of_the_last_video: ', ex)


# function for getting links to preview images (a crutch due to the large nesting of div and helplessness of requests)
def getting_a_preview_of_the_video(response):
    try:
        getting_a_preview_of_the_video = []
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('script')
        i = 1
        for link in links:
            if "image: '" in str(link):
                getting_a_preview_of_the_video += [str(link).split("'")[x] for x in range(len(str(link).split("'"))) if
                                                   'jpg' in str(link).split("'")[x]]
        getting_a_preview_of_the_video = ''.join(getting_a_preview_of_the_video)
        return getting_a_preview_of_the_video
    except Exception as ex:
        logging.error('ERROR in getting_a_preview_of_the_video: ', ex)


# a function for getting a link to download a video (a crutch due to the large nesting of div and helplessness of requests)
def getting_a_link_to_download_a_video(response):
    try:
        getting_a_link_to_download_a_video = []
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            if 'HD качестве' in str(link):
                href = link.get('href')
                if href:
                    if '.mp4' in str(href):
                        getting_a_link_to_download_a_video = str(
                            href) + f'&amp;file=mob.porno365.bond_{countlastvideo}_hd.mp4&amp;downloading'
        return getting_a_link_to_download_a_video
    except Exception as ex:
        logging.error('ERROR in getting_a_link_to_download_a_video: ', ex)


# the function of uploading photo to a given url
def uploading_photo(urldownloadphoto, folder_path):
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


# the function of uploading video to a given url
def uploading_video(urldownloadvideo, folder_path):
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


# the main function of uploading videos to the channel
async def sending_to_the_channel(namelastvideo, urltags, caption):
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
                                       caption=f'📰 {caption}\n\n[👉 PORNO365, ПОДПИШИСЬ!](https://t.me/+gFS3rVOCtfM0Zjdi)',
                                       attributes=(DocumentAttributeVideo(183, 1280, 720),), supports_streaming=True,
                                       part_size_kb=1024)
        logging.info(f'Видео {countlastvideo}.mp4  и фото {countlastvideo}.jpg выгруженно на канал.')
    except Exception as ex:
        logging.error('ERROR in sending to the chanel: ', ex)


# the function of deleting files that have already been uploaded to the channel
def delete_past_content():
    try:
        files_to_delete = [f'videos/{countlastvideo}.jpg', f'videos/{countlastvideo}.mp4']
        for file_name in files_to_delete:
            file_path = os.path.join(file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        logging.info("Video {countlastvideo}.mp4 and photo {countlastvideo}.jpg successfully deleted.\n\n")
    except Exception as ex:
        logging.error('ERROR in files_to_delete: ', ex)


# the main function of starting the bot and setting the chronology of code execution
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
        # checking for the appearance of a new video
        if title_of_the_last_video(tree) != f'Видео {countlastvideo} находится в процессе подготовки!':
            logging.info('Starting to prepare the post...')
            uploading_photo(getting_a_preview_of_the_video(response), 'videos')
            uploading_video(getting_a_link_to_download_a_video(response), 'videos')
            await sending_to_the_channel(title_of_the_last_video(tree),
                                         getting_the_tags_of_the_last_video(tree),
                                         get_a_description_for_the_video(tree))
            delete_past_content()
            countlastvideo += 1
        time.sleep(180)


if __name__ == "__main__":
    countlastvideo = 36544
    actual_url = "http://mob.porno365.bond/"
    asyncio.run(main(actual_url, countlastvideo))
