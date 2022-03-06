HEADERS = {'X-User-Store':'S801',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/98.0.4758.102 Safari/537.36'}


def get_logger(name):
    """
    Shortcut for getting debug logger
    :param name: str; name of logger
    :return: logging.Logger; Logger of logging.DEBUG level
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(Formatter(fmt='[%(name)s: %(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(stream_handler)

    if 'log' not in os.listdir():
        os.mkdir('log')

    file_handler = logging.FileHandler(f'log/{datetime.date.today()}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter(fmt='[%(name)s: %(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger


def cat_types():
    # Спарсим Json файл с информацией по категориям товаров
    cat_types_json = requests.get('https://5ka.ru/api/v5/categories/?type=category', headers = HEADERS).json()

    # Преобразуем нужные данные в словарь, ключи - Категории, значения - их Id
    cat_types_dict = {}
    for cat in cat_types_json:
            cat_types_dict[cat['name']] = cat['id']

def closest_store(lat, lon):
    r = requests.get(f'https://5ka.ru/api/v3/stores/?lat={lat}&lon={lon}&radius=1500').json()
    store = sorted(r['results'], key=lambda x: x["distance"])[0]
    return store


def process_image(product):
      
    prod_image = Image.open(urlopen(product['img_link']))
    title_font = ImageFont.truetype('RobotoCondensed-Bold.ttf', 40)

    image_editable = ImageDraw.Draw(prod_image)
    image_editable.multiline_text((10, 10), f'''{product['name']}\nЦена по скидке: {product['current_prices']['price_promo__min']} руб''', font=title_font, fill=(0, 0, 0))
 
    return prod_image