import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule
import time
import threading

bot = telebot.TeleBot('6573749748:AAHkgu9YEZrSoO4azALlhsJBOTpuQaciMwA')


# Функция для осуществления рассылки
def newsletter():
    connection = sqlite3.connect('my_database5.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER,
    sign INTEGER
    )
    ''')
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    for user_id in users:
        try:
            bot.send_message(user_id[0], horoscopes[user_id[1]])
        except:
            pass
    connection.commit()
    connection.close()


# Функция для парсинга гороскопов
def horoscope_parcing(horoscopes):
    link = 'https://retrofm.ru/goroskop'
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'lxml')
    block = soup.find('div', id='all_wrapper')
    horoscope_block = block.find('div', class_='horoscope_list')
    horoscope_list = horoscope_block.find_all('div', class_='text_box')
    for predict in horoscope_list:
        horoscopes.append(predict.text)


# Разделение потоков, чтобы парсинг, рассылка и основной функционал бота могли работать вместе
def timee():
    while True:
        schedule.run_pending()
        time.sleep(1)


horoscopes = []
horoscope_parcing(horoscopes)
schedule.every(10).seconds.do(horoscope_parcing, horoscopes=[])
schedule.every(10).seconds.do(newsletter)
threading.Thread(target=timee).start()


# Запуск бота
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower() == '/start' or message.text.lower() == 'привет' or message.text.lower() == 'начало' or message.text.lower() == 'начать' or message.text.lower() == 'запуск':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Натальная карта')
        btn2 = types.KeyboardButton('Совместимость')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Гороскоп на день')
        markup.row(btn3)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Что бы ты хотел узнать?',
                         reply_markup=markup)
        bot.register_next_step_handler(message, choose_option)


# Обработка запроса
@bot.message_handler(content_types=['text'])
def choose_option(message):
    # Пользователь уже начинал пользоваться ботом, но потом очистил историю
    if message.text.lower() == '/start':
        start(message)
    # Помощь
    elif message.text.lower() == '/help' or message.text.lower() == 'help' or message.text.lower() == 'помощь' or message.text.lower() == 'инфо' or message.text.lower() == 'информация':
        bot.send_message(message.chat.id,
                         'С помощью этого бота ты можешь узнать свою натальную карту, совместимость или гороскоп. Для этого воспользуйся панелью управления снизу. Надеемся, наш бот тебе понравится:)')
        bot.register_next_step_handler(message, choose_option)
    # Натальная карта
    elif message.text.lower() == '/natal_chart' or message.text.lower() == 'натальная карта' or message.text.lower() == 'natal chart':
        bot.send_message(message.chat.id, 'Извини, эта функция появится позже')
        bot.register_next_step_handler(message, choose_option)
    # Совместимость
    elif message.text.lower() == 'совместимость' or message.text.lower() == '/compatibility' or message.text.lower() == 'compatibility':
        bot.send_message(message.chat.id, 'Введите два знака зодиака в формате: Рыбы Водолей')
        bot.register_next_step_handler(message, compatibility)
    # Гороскоп
    elif message.text.lower() == 'гороскоп' or message.text.lower() == 'horoscope' or message.text.lower() == '/daily_horoscope' or message.text.lower() == 'гороскоп на день' or message.text.lower() == 'daily_horoscope':
        bot.send_message(message.chat.id, 'Какой знак гороскопа тебя интереcует?')
        bot.register_next_step_handler(message, horoscope_sign)
    # Отписка от рассылки
    elif message.text.lower() == '/unsubscribe' or message.text.lower() == 'отписка':
        bot.send_message(message.chat.id, 'Ты уверен?')
        bot.register_next_step_handler(message, unsubscribe)
    # Чепуха
    else:
        bot.send_message(message.chat.id,
                         'К сожалению, я не умею выполнять эту команду:( Чтобы узнать, что я могу, введи команду /help')
        bot.register_next_step_handler(message, choose_option)


# Функция для натальной карты
def natal_chart(message):
    pass

#парсинг совместимости
def compatibility_parcing(num):
    URL = 'https://www.nur.kz/esoterics/astrology/1824471-lubov-znakov-zodiaka-kak-lubit-kazdyj-znak/'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    collection = soup.find_all('p', class_="align-left formatted-body__paragraph")[1:-1]
    merged_collection = []
    for i in range(1, len(collection), 2):
        merged_collection.append(collection[i - 1].text + collection[i].text)
    return f'{merged_collection[num]}'

# Функция для совместимости
def compatibility(message):
    mapa = {
        "овен": 0,
        "телец": 1,
        "близнецы": 2,
        "рак": 3,
        "лев": 4,
        "дева": 5,
        "весы": 6,
        "скорпион": 7,
        "стрелец": 8,
        "козерог": 9,
        "водолей": 10,
        "рыбы": 11,
    }
    mass = [[91, 81, 72, 81, 97, 84, 83, 76, 92, 82, 82, 91],
            [72, 87, 73, 83, 88, 92, 92, 98, 81, 89, 83, 91],
            [83, 73, 84, 67, 81, 93, 89, 93, 98, 82, 82, 93],
            [91, 93, 77, 83, 82, 84, 94, 91, 82, 96, 84, 90],
            [99, 91, 68, 71, 87, 86, 79, 98, 90, 76, 97, 83],
            [71, 69, 75, 81, 73, 75, 74, 98, 72, 61, 72, 67],
            [82, 93, 93, 78, 89, 85, 91, 64, 88, 92, 96, 81],
            [72, 60, 58, 89, 92, 76, 77, 94, 92, 100, 88, 97],
            [84, 72, 100, 71, 100, 82, 92, 100, 100, 79, 100, 71],
            [82, 86, 71, 82, 83, 85, 81, 100, 93, 84, 82, 67],
            [100, 82, 93, 66, 92, 67, 100, 89, 100, 92, 77, 100],
            [85, 82, 81, 83, 95, 100, 100, 100, 74, 93, 93, 100]
            ]

    index = message.text.find(" ")
    first_sign = message.text[:index].lower()
    second_sign = message.text[index + 1:].lower()
    i = 0
    j = 0
    try:
        i = mapa[first_sign]
        j = mapa[second_sign]
    except KeyError:
        bot.send_message(message.chat.id, 'Такого знака зодиака нет, попробуй еще раз')
        bot.register_next_step_handler(message, horoscope_sign)
        return 0

    result = f'Ваша совместимость: {(mass[i][j])} %'
    bot.send_message(message.chat.id, result)
    bot.send_message(message.chat.id, f'{first_sign}: \n')
    bot.send_message(message.chat.id, compatibility_parcing(i))
    bot.send_message(message.chat.id, f'{second_sign}: \n')
    bot.send_message(message.chat.id, compatibility_parcing(j))
    bot.register_next_step_handler(message, choose_option)

    return 0

# Функция для отправки гороскопа
def horoscope_sign(message):
    cnt = 0
    sign_of_user = 0
    if message.text.lower() == 'овен':
        bot.send_message(message.chat.id, horoscopes[1])
        sign_of_user = 1
    elif message.text.lower() == 'телец':
        bot.send_message(message.chat.id, horoscopes[2])
        sign_of_user = 2
    elif message.text.lower() == 'близнецы':
        bot.send_message(message.chat.id, horoscopes[3])
        sign_of_user = 3
    elif message.text.lower() == 'рак':
        bot.send_message(message.chat.id, horoscopes[4])
        sign_of_user = 4
    elif message.text.lower() == 'лев':
        bot.send_message(message.chat.id, horoscopes[5])
        sign_of_user = 5
    elif message.text.lower() == 'дева':
        bot.send_message(message.chat.id, horoscopes[6])
        sign_of_user = 6
    elif message.text.lower() == 'весы':
        bot.send_message(message.chat.id, horoscopes[7])
        sign_of_user = 7
    elif message.text.lower() == 'скорпион':
        bot.send_message(message.chat.id, horoscopes[8])
        sign_of_user = 8
    elif message.text.lower() == 'стрелец':
        bot.send_message(message.chat.id, horoscopes[9])
        sign_of_user = 9
    elif message.text.lower() == 'козерог':
        bot.send_message(message.chat.id, horoscopes[10])
        sign_of_user = 10
    elif message.text.lower() == 'водолей':
        bot.send_message(message.chat.id, horoscopes[11])
        sign_of_user = 11
    elif message.text.lower() == 'рыбы':
        bot.send_message(message.chat.id, horoscopes[12])
        sign_of_user = 12
    else:
        bot.send_message(message.chat.id, 'Такого знака нет:( Попробуй еще раз')
        bot.register_next_step_handler(message, horoscope_sign)
        cnt = 1
    # Предложение подписаться на рассылку
    if cnt == 0:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data=f'yes {sign_of_user}'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='no'))
        bot.send_message(message.chat.id, 'Хочешь подписаться на ежедневную рассылку?', reply_markup=markup)
    if cnt == 0:
        bot.register_next_step_handler(message, choose_option)


# Функция отписки от рассылки
def unsubscribe(message):
    if message.text.lower() == 'да' or message.text.lower() == 'yes':
        bot.send_message(message.chat.id, 'Подписка отменена')
        connection = sqlite3.connect('my_database5.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Users WHERE id=?", (message.chat.id,))
        connection.commit()
        connection.close()
    else:
        bot.send_message(message.chat.id, 'Рад, что ты решил не отписываться')
    bot.register_next_step_handler(message, choose_option)


# Функция оформления подписки
@bot.callback_query_handler(func=lambda callback: True)
def subscription(callback):
    if callback.data[0:3] == 'yes':
        user_id = callback.message.chat.id
        sign_of_user = int(callback.data[3:])
        connection = sqlite3.connect('my_database5.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER,
        sign INTEGER
        )
        ''')
        cursor.execute('INSERT INTO Users (id, sign) VALUES (?, ?)', (user_id, sign_of_user))
        connection.commit()
        connection.close()
        bot.send_message(callback.message.chat.id,
                         'Подписка успешно оформлена. Если захочешь отписаться, используй команду /unsubscribe')
    else:
        bot.send_message(callback.message.chat.id,
                         'Очень жаль, что ты не хочешь оформить подписку. Надеемся, ты передумаешь')
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


bot.polling(none_stop=True)