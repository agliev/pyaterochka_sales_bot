import os
import sys
import logging
import datetime
import requests
from urllib.request import urlopen
from logging import StreamHandler, Formatter
from PIL import Image, ImageFont, ImageDraw

HEADERS = {'X-User-Store': 'S801',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/98.0.4758.102 Safari/537.36'}


def get_logger(name, write_local=False):
    """
    Shortcut for getting debug logger
    :param write_local: bool
    :param name: str; name of logger
    :return: logging.Logger; Logger of logging.DEBUG level
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(Formatter(fmt='[%(name)s: %(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(stream_handler)

    if write_local:
        if 'log' not in os.listdir():
            os.mkdir('log')

        file_handler = logging.FileHandler(f'log/{datetime.date.today()}.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(Formatter(fmt='[%(name)s: %(asctime)s: %(levelname)s] %(message)s'))
        logger.addHandler(file_handler)

    logger.propagate = False

    return logger


def get_categories():
    """
    Gets categories from 5ka API
    :return: dict
    """
    categories_json = requests.get('https://5ka.ru/api/v5/categories/?type=category',
                                   headers=HEADERS).json()

    categories_dict = {}
    for category in categories_json:
        categories_dict[category['name']] = category['id']

    return categories_dict


def get_closest_store(lat, lon, radius=1500):
    """
    Gets list of closest stores from 5ka API by lat and lon
    :param radius: int
    :param lat: float
    :param lon: float
    :return: dict
    """

    response = requests.get(f'https://5ka.ru/api/v3/stores/?lat={lat}&lon={lon}&radius={radius}').json()
    store = sorted(response['results'],
                   key=lambda x: x["distance"])[0]

    return store


def get_product_image(product):
    """
    TODO: implement product as class, transform to class method
    Gets image from 5ka product and transforms it
    :param product: dict
    :return: PIL.Image
    """
    image = Image.open(urlopen(product['img_link']))
    title_font = ImageFont.truetype('RobotoCondensed-Bold.ttf', 40)

    image_edited = ImageDraw.Draw(image)
    image_edited.multiline_text((10, 10),
                                f'''{product['name']}\n
                                Цена по скидке: {product['current_prices']['price_promo__min']} руб.''',
                                font=title_font,
                                fill=(0, 0, 0))
 
    return image
