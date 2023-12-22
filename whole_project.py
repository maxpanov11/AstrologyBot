# Здесь лежит весь проект целиком, сделано просто для удобства, чтобы можно было скоировать и сразу запустить

import datetime
import json
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule
import time
import threading
import json2html

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

# парсинг совместимости
def compatibility_parcing(merged_collection):
    URL = 'https://www.nur.kz/esoterics/astrology/1824471-lubov-znakov-zodiaka-kak-lubit-kazdyj-znak/'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    collection = soup.find_all('p', class_="align-left formatted-body__paragraph")[1:-1]
    for i in range(1, len(collection), 2):
        merged_collection.append(collection[i - 1].text + collection[i].text)


# Разделение потоков, чтобы парсинг, рассылка и основной функционал бота могли работать вместе
def timee():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Массив с гороскопами
horoscopes = []
horoscope_parcing(horoscopes)
# Массив с совместимостью
merged_collection = []
compatibility_parcing(merged_collection)
# Пока что парсинг и рассылка выполняется каждые 10 секунд, это сделано для простоты отладки функции подписки. 
# Интервал легко поменять на раз в день, немного подкорректировав две следующие функции
schedule.every(10).seconds.do(horoscope_parcing, horoscopes=[])
schedule.every(10).seconds.do(newsletter)
threading.Thread(target=timee).start()


# Запуск бота
@bot.message_handler(content_types=['text'])
def start(message):
    map_start = ['/start', 'привет', 'начало', 'начать', 'запуск']
    if message.text.lower() in map_start:
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Натальная карта')
        btn2 = types.KeyboardButton('Совместимость')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Гороскоп на день')
        markup.row(btn3)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Что бы ты хотел узнать?',
                         reply_markup=markup)
        bot.register_next_step_handler(message, choose_option)
    else:
        bot.send_message(message.chat.id, 'Чтобы начать, введи команду /start')

# Обработка запроса
@bot.message_handler(content_types=['text'])
def choose_option(message):
    # Пользователь уже начинал пользоваться ботом, но потом очистил историю
    if message.text.lower() == '/start':
        start(message)
    # Помощь
    elif message.text.lower() == '/help' or message.text.lower() == 'help' or message.text.lower() == 'помощь' or message.text.lower() == 'инфо' or message.text.lower() == 'информация':
        bot.send_message(message.chat.id,
                         '''С помощью этого бота ты можешь узнать свою натальную карту, совместимость или гороскоп. \n\nДля этого воспользуйся панелью управления снизу. \n\nПолный список команд можно увидеть,
нажав на кнопку "Меню" слева. \n\nНадеемся, наш бот тебе понравится:)''')
        bot.register_next_step_handler(message, choose_option)
    # Натальная карта
    elif message.text.lower() == '/natal_chart' or message.text.lower() == 'натальная карта' or message.text.lower() == 'natal chart':
        bot.send_message(message.chat.id, 'Введите время в формате DD:MM:YYYY HH:MM и город')
        bot.register_next_step_handler(message, natal_chart)
    # Совместимость
    elif message.text.lower() == 'совместимость' or message.text.lower() == '/compatibility' or message.text.lower() == 'compatibility':
        markup = types.InlineKeyboardMarkup()
        btn1 = (types.InlineKeyboardButton('Да', callback_data='sign2yes'))
        btn2 = (types.InlineKeyboardButton('Нет', callback_data='sign2no'))
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Ты знаешь свой знак гороскопа и знак своего партнера?', reply_markup=markup)
    # Гороскоп
    elif message.text.lower() == 'гороскоп' or message.text.lower() == 'horoscope' or message.text.lower() == '/daily_horoscope' or message.text.lower() == 'гороскоп на день' or message.text.lower() == 'daily_horoscope':
        markup = types.InlineKeyboardMarkup()
        btn1 = (types.InlineKeyboardButton('Да', callback_data='sign1yes'))
        btn2 = (types.InlineKeyboardButton('Нет', callback_data='sign1no'))
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Ты знаешь свой знак гороскопа?', reply_markup=markup)
    # Знак зодиака
    elif message.text.lower() == 'знак' or message.text.lower() == 'sign' or message.text.lower() == '/sign':
        bot.send_message(message.chat.id, 'Введи день и месяц рождения в формате: ДД.ММ')
        bot.register_next_step_handler(message, date_to_sign)
    # Отписка от рассылки
    elif message.text.lower() == '/unsubscribe' or message.text.lower() == 'отписка':
        markup = types.InlineKeyboardMarkup()
        btn1 = (types.InlineKeyboardButton('Да', callback_data='unsyes'))
        btn2 = (types.InlineKeyboardButton('Нет', callback_data='unsno'))
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Ты уверен?', reply_markup=markup)
        bot.register_next_step_handler(message, choose_option)
    # Смена знака гороскопа 
    elif message.text.lower() == '/change_sign':
        bot.send_message(message.chat.id, 'Введи новый знак зодиака для подписки')
        bot.register_next_step_handler(message, change_of_sign)
    # Чепуха
    else:
        bot.send_message(message.chat.id,
                         'К сожалению, я не умею выполнять эту команду:( Чтобы узнать, что я могу, введи команду /help')
        bot.register_next_step_handler(message, choose_option)

#Перевод даты в знак гороскопа
def date_to_sign(message, k=0, two_signs=''):
    signs = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы']
    dates = [[20, 10, 11], [20, 11, 12], [20, 12, 1], [20, 1, 2], [20, 2, 3], [21, 3, 4],
             [22, 4, 5], [23, 5, 6], [23, 6, 7], [23, 7, 8], [22, 8, 9], [21, 9, 10]]
    separators = ['.', ',', ':', '/', ';', ' ']
    mistake = 0
    if len(message.text) < 3 or len(message.text) > 5:
        bot.send_message(message.chat.id, 'Похоже, ты ввел дату в неправильном формате, попробуй еще раз')
        mistake = 1
    elif message.text[1] not in separators and message.text[2] not in separators:
        bot.send_message(message.chat.id, 'Не хватает разделителя между днем и месяцем, попробуй еще раз')
        mistake = 1
    elif message.text[1] in separators and message.text[0] >= '1' and message.text[0] <= '9':
        if len(message.text) == 3:
            if message.text[2] >= '1' and message.text[2] <= '9':
                month = int(message.text[2])
                day = int(message.text[0])
            else:
                bot.send_message(message.chat.id, 'Что-то не так с месяцем, попробуй еще раз')
                mistake = 1
        elif len(message.text) == 4:
            if message.text[2] == '0' and message.text[3] >= '1' and message.text[3] <= '9':
                month = int(message.text[3])
                day = int(message.text[0])
            elif message.text[2] == '1' and message.text[3] >= '0' and message.text[3] <= '2':
                month = int(message.text[2:4])
                day = int(message.text[0])
            else:
                bot.send_message(message.chat.id, 'Что-то не так с месяцем, попробуй еще раз')
                mistake=1
                    
        else:
            bot.send_message(message.chat.id, 'Похоже, ты ввел дату в неправильном формате, попробуй еще раз')
            mistake = 1
    elif message.text[2] in separators and len(message.text) >= 4:
        if message.text[0] == '0' and message.text[1] >= '1' and message.text[1] <= '9':
            day = int(message.text[1])
        elif message.text[0] >= '1' and message.text[0] <= '3' and message.text[1] >= '0' and message.text[1] <= '9':
            day = int(message.text[0:2])
            if day > 31:
                bot.send_message(message.chat.id, 'Введен неверный день')
                mistake = 1
        else:
            bot.send_message(message.chat.id, 'Введен неверный день')
            mistake = 1
        if len(message.text) == 5 and mistake != 1:
            if message.text[3] == '0' and message.text[4] >= '1' and message.text[4] <= '9':
                month = int(message.text[4])
            elif message.text[3] == '1' and message.text[4] >= '0' and message.text[4] <= '2':
                month = int(message.text[3:5])
            else:
                bot.send_message(message.chat.id, 'Введен неверный месяц')
                mistake = 1
        elif mistake != 1:
            if message.text[3] >= '1' and message.text[3] <= '9':
                month = int(message.text[3])
            else:
                bot.send_message(message.chat.id, 'Введен неверный месяц')
                mistake = 1
    else:
        bot.send_message(message.chat.id, 'Похоже, ты ввел дату в неправильном формате, попробуй еще раз')
        mistake = 1
    if mistake == 0:
        sign=signs[(day<=dates[month-1][0])*dates[month-1][1]+(day>dates[month-1][0])*dates[month-1][2]-1]
        if k != 2:
            bot.send_message(message.chat.id, f'Твой знак зодиака: {sign}')
        if k == 0:
            bot.register_next_step_handler(message, choose_option)
        elif k == 1:
            message.text = sign
            horoscope_sign(message)
        elif k == 2:
            if two_signs == '':
                two_signs = sign
                bot.send_message(message.chat.id, f'Твой знак зодиака: {sign}')
                bot.send_message(message.chat.id, 'Введи день и месяц рождения своего партнера в формате: ДД.ММ')
                bot.register_next_step_handler(message, date_to_sign, 2, two_signs)
            else:
                bot.send_message(message.chat.id, f'Знак зодиака твоего партнера: {sign}')
                two_signs+= ' ' + sign
                message.text = two_signs
                compatibility(message)
                
    else:
         bot.register_next_step_handler(message, date_to_sign, k)

# Функция для обработки знает пользователь свой знак или нет
@bot.callback_query_handler(func=lambda callback: callback.data[0:4] == 'sign')
def processing_of_sign(callback):
    if callback.data[5:] == 'yes':
        if callback.data[4] == '1':
            mes = bot.send_message(callback.message.chat.id, 'Какой знак гороскопа тебя интереcует?')
            bot.register_next_step_handler(mes, horoscope_sign)
        else:
            mes = bot.send_message(callback.message.chat.id, 'Введите два знака зодиака в формате: Рыбы Водолей')
            bot.register_next_step_handler(mes, compatibility)
    else:
        if callback.data[4] == '1':
            mes = bot.send_message(callback.message.chat.id, 'Введи день и месяц рождения в формате: ДД.ММ')
            bot.register_next_step_handler(mes, date_to_sign, 1)
        else:
            mes = bot.send_message(callback.message.chat.id, 'Введи свой день и месяц рождения в формате: ДД.ММ')
            bot.register_next_step_handler(mes, date_to_sign, 2)
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


#Функция обработок ошибок в написании знака
def mistakes_corrector(word):
    if len(word) > 10 or len(word) < 2:
        return 0
    else:
        signs = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы']
        dist = []
        for sign in signs:
            if abs(len(sign)-len(word)) <= 2:
                leven = [[0] * (len(word)+1) for i in range(len(sign)+1)]
                for i in range(1, (len(word)+1)):
                    leven[0][i] = i
                for j in range(1, (len(sign)+1)):
                        leven[j][0] = j
                for i in range(1, len(sign)+1):
                    for j in range(1, len(word)+1):
                        leven[i][j] = min(leven[i-1][j]+1, leven[i][j-1]+1, leven[i-1][j-1] + (word[j-1]!=sign[i-1]))
                if leven[-1][-1] == 1:
                    return sign
                else:
                    dist.append([leven[-1][-1], sign])
        if min(dist)[0] <= 2:
            return min(dist)[1]
        else:
            return 0


# Функция для процессинга функции исправления ошибок
@bot.callback_query_handler(func=lambda callback: callback.data[0:3] == 'cor')
def mistakes_processing(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if callback.data[3:6] == 'yes':
        if callback.data[6] == '1':
            callback.message.text = callback.data.split()[1]
            horoscope_sign(callback.message)
        else:
            callback.message.text = callback.data[8:]
            compatibility(callback.message)
    else:
        if callback.data[5] == '1':
            mes = bot.send_message(callback.message.chat.id, 'Пожалуйста, введи знак зодика еще раз')
            bot.register_next_step_handler(mes, horoscope_sign)
        else:
            mes = bot.send_message(callback.message.chat.id, 'Пожалуйста, введи пару знаков зодика еще раз')
            bot.register_next_step_handler(mes, compatibility)

# Функция для натальной карты
def natal_chart(message):
    try:
        user_input = message.text.split()

        if len(user_input) < 3:
            bot.reply_to(message, "Пожалуйста, укажите дату, время и место (город) в правильном формате.")
            return

        birth_date = user_input[0]  # Date format: DD:MM:YYYY
        birth_time = user_input[1]  # Time format: HH:MM

        parsed_date = datetime.datetime.strptime(birth_date + " " + birth_time, "%d:%m:%Y %H:%M")

    # Создание нового объекта datetime с нужной датой (2000-01-01) и временем (00:00:00)
        new_date = datetime.datetime(2000, 1, 1)
    # Конечный формат даты и времени
        formatted_date = new_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # Конечная точка API и параметры для создания натальной карты
        api_endpoint = 'https://api.astroapi.cloud/horoscope/natal/calculate'
        api_key = 'MndMdGc4by9RWlN1RVFlcSsrQXVDdz09Lit5c3lXbGdDVHF1aU1qalcxSFJLNmc9PQ=='

    # Сделать запрос к API
        response = requests.post(api_endpoint, json={"dateTime": formatted_date,
                                                 "latitude": 50.8476424,
                                                 "longitude": 4.3571696}, headers={'X-Api-Key': api_key})

        if response.status_code == 200:
            natal_chart = response.json()  # Предполагаем, что API возвращает данные в формате JSON
            html = json2html.json2html.convert(json=natal_chart)
            htmlFile = open("GFG-1.html", "w")
            htmlFile.write(html)
            htmlFile.close()

            f = open("GFG-1.html", "rb")

            bot.send_document(chat_id=message.chat.id, document=f)
    except:
        bot.reply_to(message, "Не удалось составить натальную карту. Пожалуйста, попробуйте снова.")
    bot.register_next_step_handler(message, choose_option)



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
        if index != -1:
            corrected_sign1 = mistakes_corrector(first_sign)
            corrected_sign2 = mistakes_corrector(second_sign)
            if corrected_sign1 != 0 and corrected_sign2 != 0:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Да', callback_data=f'coryes2 {corrected_sign1} {corrected_sign2}'))
                markup.add(types.InlineKeyboardButton('Нет', callback_data='corno2'))
                bot.send_message(message.chat.id, f'Похоже, ты ошибся в знаках зодиака. Возможно ты имел в виду: {corrected_sign1} {corrected_sign2}', reply_markup=markup) 

            else:
                bot.send_message(message.chat.id, 'Такой пары знаков зодиака нет, попробуй еще раз')
                bot.register_next_step_handler(message, compatibility)
        else:
            bot.send_message(message.chat.id, 'Такой пары знаков зодиака нет, попробуй еще раз')
            bot.register_next_step_handler(message, compatibility)
    else:
        result = f'Ваша совместимость: {(mass[i][j])} %'
        bot.send_message(message.chat.id, result)
        bot.send_message(message.chat.id, f'{first_sign}: \n')
        bot.send_message(message.chat.id, merged_collection[i])
        if i != j:
            bot.send_message(message.chat.id, f'{second_sign}: \n')
            bot.send_message(message.chat.id, merged_collection[j])
        bot.register_next_step_handler(message, choose_option)


# Функция для отправки гороскопа
def horoscope_sign(message):
    map_sign = {'овен': 1, 'телец': 2, 'близнецы': 3, 'рак': 4, 'лев': 5, 'дева': 6, 'весы': 7, 'скорпион': 8, 'стрелец': 9, 'козерог': 10, 'водолей': 11, 'рыбы': 12}
    sign_of_user = map_sign.get(message.text.lower(), 0)
    cnt = 0
    if sign_of_user != 0:
        bot.send_message(message.chat.id, horoscopes[sign_of_user])
    else:
        corrected_sign = mistakes_corrector(message.text.lower())
        if corrected_sign == 0:
            bot.send_message(message.chat.id, 'Такого знака нет:( Попробуй еще раз')
            bot.register_next_step_handler(message, horoscope_sign)
            cnt = 1
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data=f'coryes1 {corrected_sign}'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='corno1'))
            bot.send_message(message.chat.id, f'Похоже, ты ошибся в знаке зодиака. Возможно ты имел в виду: {corrected_sign}', reply_markup=markup)
            cnt = 1
    # Предложение подписаться на рассылку
    if cnt == 0:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data=f'subyes {sign_of_user}'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='subno'))
        bot.send_message(message.chat.id, 'Хочешь подписаться на ежедневную рассылку?', reply_markup=markup)
    if cnt == 0:
        bot.register_next_step_handler(message, choose_option)
        
        
# Функция отписки от рассылки
@bot.callback_query_handler(func=lambda callback: callback.data[0:3] == 'uns')
def unsubscribe(callback):
    if callback.data[3:6] == 'yes':
        user_id = callback.message.chat.id
        connection = sqlite3.connect('my_database5.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER,
        sign INTEGER
        )
        ''')
        exist = cursor.execute('SELECT * FROM Users where id=?', (user_id,))
        if exist.fetchone() is None:
            bot.send_message(callback.message.chat.id, 'У тебя и так нет подписки')
        else:
            cursor.execute("DELETE FROM Users WHERE id=?", (user_id,))
            connection.commit()
            bot.send_message(callback.message.chat.id, 'Подписка отменена')
        connection.close()       
    else:
        bot.send_message(callback.message.chat.id, 'Рад, что ты решил не отписываться')
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


# Функция оформления подписки
@bot.callback_query_handler(func=lambda callback: callback.data[0:3] == 'sub')
def subscription(callback):
    if callback.data[3:6] == 'yes':
        user_id = callback.message.chat.id
        inf_arr = callback.data.split()
        sign_of_user = int(inf_arr[1])
        connection = sqlite3.connect('my_database5.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER,
        sign INTEGER
        )
        ''')
        exist = cursor.execute('SELECT * FROM Users where id=?', (user_id,))
        if exist.fetchone() is None:
            cursor.execute('INSERT INTO Users (id, sign) VALUES (?, ?)', (user_id, sign_of_user))
            connection.commit()
            connection.close()
            bot.send_message(callback.message.chat.id,
                         'Подписка успешно оформлена. Если захочешь отписаться, используй команду /unsubscribe')
        else:
            signs = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы']
            sign = signs[int(cursor.execute('SELECT sign FROM Users where id=?', (user_id,)).fetchall()[0][0])-1] 
            bot.send_message(callback.message.chat.id,
                                   f'У тебя уже оформлена подписка. Выбранный знак зодиака: {sign}. Если хочешь поменять знак зодиака, используй команду /change_sign')
            connection.close()
            
    else:
        bot.send_message(callback.message.chat.id,
                         'Очень жаль, что ты не хочешь оформить подписку. Надеемся, ты передумаешь')
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

# Смена знака зодиака в подписке
def change_of_sign(message):
    map_sign = {'овен': 1, 'телец': 2, 'близнецы': 3, 'рак': 4, 'лев': 5, 'дева': 6, 'весы': 7, 'скорпион': 8, 'стрелец': 9, 'козерог': 10, 'водолей': 11, 'рыбы': 12}
    sign_of_user = map_sign.get(message.text.lower(), 0)
    if sign_of_user == 0:
        bot.send_message(message.chat.id, 'Такого знака нет:( Попробуй еще раз')
        bot.register_next_step_handler(message, change_of_sign)
    else:
        user_id = message.chat.id
        connection = sqlite3.connect('my_database5.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER,
        sign INTEGER
        )
        ''')
        cursor.execute("UPDATE Users SET sign = ? WHERE id = ?", (sign_of_user, user_id))
        connection.commit()
        connection.close()
        bot.send_message(message.chat.id, 'Знак изменен')
        bot.register_next_step_handler(message, choose_option)
bot.polling(none_stop=True)
