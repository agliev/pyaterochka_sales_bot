import telebot
from telebot import types
from telebot.types import InputMediaPhoto
from secrets import TOKEN
from functions import get_logger, get_categories, get_closest_store, get_products, get_product_image

cat_types_dict = get_categories()

bot = telebot.TeleBot(TOKEN)
logger = get_logger('pyaterochka_bot')

logger.debug(f'Initialized')
prod_category = "Замороженные продукты"


@bot.message_handler(commands=["start", 'старт'])
def welcome(message):

    # Первые кнопки, созданы в рамках теста
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cat = types.KeyboardButton('/categories')
    aksii = types.KeyboardButton('/aksii')

    markup.add(cat, aksii)

    # Отправим пользователям базовую информацию о функционале бота
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.first_name}. Данный бот поможет узнать - на какие товары сегодня проходит акция в ближайшем магазине Пятерочка.С помощью предложенных команд вы можете выбрать нужную категорию товаров, а после узнать о наличии товаров по акции :)\n\nУзнать о выбранной категории и сменить ее можно через команду - /categories\nЕсли хотите ухнать о скидках в ближейшей Пятерочке, отправь /aksii.\n\nМожете как писать команды, так и нажимать на кнопки :)',
                     reply_markup=markup)

    logger.debug(f'Called function welcome {message.from_user.name}')


@bot.message_handler(commands=['categories', 'категории'])
def first_step(message):
    
    # Кнопки созданы с целью облегчить указание польщователем наиболее популярных категорий продуктов
        # buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # first = types.KeyboardButton('На кассе')
        # second = types.KeyboardButton('Замороженные продукты')
        # buttons.add(first, second)

    bot.send_message(message.from_user.id,
                     f'Выбранная категория продуктов на данный момент - {prod_category}.\n\nЕсли вы хотите сменить категорию, выберите интересующую вас и отправьте ее название\n\nНазвания категорий:\nНа кассе, Безопасность, Молочные продукты и яйца, Овощи и фрукты, Хлеб и выпечка, Готовые блюда и кулинария, Мясо и птица, Колбаса и сосиски, Замороженные продукты, Рыба и морепродукты, Бакалея, Снеки, Сладости, Чай, кофе и какао, Напитки, Консервы и соленья, Товары для животных, Гигиена и уход, Товары для детей, Товары для дома')  # , reply_markup = buttons)

    bot.register_next_step_handler(message, category)
    logger.debug(f'Called function first_step {message.from_user.id}')


def category(message):
    global prod_category
    text = message.text.lower().strip()
    text = text[0].upper() + text[1:]
    print("Выбрана категория " + text)
    if text in cat_types_dict.keys():
        prod_category = text

    else:
        bot.send_message(message.from_user.id,
                         'Вы указали несуществующую категорию, пожалуйста, попробуйте еще раз - /categories')

    # Кнопки созданы с целью облегчить указание польщователем желаемой категории продуктов
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cat = types.KeyboardButton('/categories')
    aksii = types.InlineKeyboardButton('/aksii', callback_data=prod_category)
    buttons.add(cat, aksii)

    bot.send_message(message.from_user.id, "Можешь получить список акций через команду - /aksii", reply_markup=buttons)
    logger.debug(f'Called function category {message.from_user.id}')


@bot.message_handler(commands=["aksii", 'акции'])
def geolocation(message):
    # Клавиатура с кнопкой запроса локации
    keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение 🌍", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Поделись местоположением - узнаешь адрес ближайшей Пятерочки со скидками",
                     reply_markup=keyboard)
    logger.debug(f'Called function geolocation {message.from_user.id}')


# Получаю локацию
@bot.message_handler(content_types=['location'])
def products(message):
    store = get_closest_store(message.location.latitude, message.location.longitude)
    bot.send_message(message.from_user.id,
                     f"""Ближайшая Пятерочка находится по адресу {store['address']}\n\nПодргружаем товары по акции...""")
    logger.debug(f'Called function products {message.from_user.id}')

    # Получаю список продуктов по заданной категории в ближайшем магазине, задав параметры при помощи api
    products = get_products(store, category=cat_types_dict[prod_category])
    media = []

    if len(products) > 0:
        for product in products:
            media.append(InputMediaPhoto(media=get_product_image(product)))

            #     Условие для отправки фото альбомами, не более 10 штук в каждом
        if (len(media) // 10) != 0:
            for i in range(len(media) // 10 + 1):
                bot.send_media_group(message.chat.id, media=media[i * 10:(i + 1) * 10])
        else:
            for i in range(len(media) // 10):
                bot.send_media_group(message.chat.id, media=media[i * 10:(i + 1) * 10])



    else:
        bot.send_message(message.from_user.id, "По данной категории в этом магазине скидок нет :(")


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def button_answer(message):
    if message.chat.type == 'private':
        if message.text == 'Станция зачечная! 🛒':
            bot.send_message(message.chat.id, "Степа - молодец, он купил молоко!")
        elif message.text == 'Просто кнопка':
            bot.send_message(message.chat.id, "Ну и зачем ты на нее нажал(а)?")
        else:
            bot.send_message(message.chat.id, "Уточните запрос-СОС")


bot.polling(none_stop=True)