from random import randrange
import requests
from lxml import html
import sys
import time
import logging

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


def get_href_last_video(url):
    # получение html кода сайта из раздела "лучшие"
    try:
        response = requests.get(url, headers=random_headers(True, url))
        tree = html.document_fromstring(response.text)
    except Exception as ex:
        logging.error('ERROR in get response: ', ex)

    # получение ссылки на последнее видео
    try:
        href_last_video = ''.join(tree.xpath('//*[@id="v429691991"]/div/div[3]/span/a/@href'))
        return href_last_video
    except Exception as ex:
        logging.error('ERROR in href_last_video: ', ex)


def get_href_for_download_video(url, tree):
    # получение ссылки для загрузки видео
    try:
        href_for_download_video = 'хуй тебе обойти этот ёбанный загрузчик, буду завтра смотреть прямую ссылку загрузки видео 👹'
        logging.info(href_for_download_video)
        return href_for_download_video
    except Exception as ex:
        logging.error('ERROR in href_for_download_video: ', ex)


def get_preview_video(url, tree):
    # получение ссылки для загрузки фото для превью видео
    try:
        preview_video = ''.join(tree.xpath(
            '/html/body/div[5]/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]/video-element/div/div[14]/div[1]/picture/img/@href'))
        logging.info('завтра сделаю ссыылку на превью ибо зарылся в либе re, можешь попробовать через суп сделать')
        return preview_video
    except Exception as ex:
        logging.error('ERROR in href_for_download_video: ', ex)


def get_tags_video(url, tree):
    # получение тэгов видео
    try:
        tag = 1
        tags_video = []
        while tree.xpath(
                f'//*[@id="hd-leftColVideoPage"]/div[1]/div[6]/div[1]/div[4]/div[2]/div[2]/div[1]/a[{tag}]/text()') != []:
            tags_video.append('#' + ''.join(tree.xpath(
                f'//*[@id="hd-leftColVideoPage"]/div[1]/div[6]/div[1]/div[4]/div[2]/div[2]/div[1]/a[{tag}]/text()')).replace(
                ' ', ''))
            tag += 1
        tags_video = ' '.join(tags_video)
        logging.info(tags_video)
        return tags_video
    except Exception as ex:
        logging.error('ERROR in get_tags_video: ', ex)


def main():
    url = 'https://rt.pornhub.com/video?o=tr'
    logging.info('The bot has started working.')
    check_on_appearance_new_video_href = ''
    while True:
        href_last_video = get_href_last_video(url)
        # проверка на появление нового видео в виде сравнения ссылок последних видео чтобы избежать дубликатов
        if href_last_video != check_on_appearance_new_video_href:
            current_href_last_video = f'https://rt.pornhub.com{href_last_video}'
            logging.info(current_href_last_video)
            try:  # получение html кода сайта с самим видео
                response = requests.get(current_href_last_video, headers=random_headers(True, url))
                tree = html.document_fromstring(response.text)
            except Exception as ex:
                logging.error('ERROR in get response: ', ex)
            get_href_for_download_video(current_href_last_video, tree)
            get_preview_video(current_href_last_video, tree)
            get_tags_video(current_href_last_video, tree)
        check_on_appearance_new_video_href = href_last_video
        time.sleep(10)


if __name__ == '__main__':
    main()
