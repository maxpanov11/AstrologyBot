import telebot
from telebot import types
import sqlite3
import schedule
import threading

from telegram_bot_calendar import DetailedTelegramCalendar

from functions.date_to_sign import date_to_sign
from functions.chinese_sign import chinese_sign
from functions.compatibility import compatibility
from functions.horoscope import horoscope_sign
from functions.natal_chart import natal_chart
from utilities.logger import logger
from utilities.horoscope_parcing import horoscope_parcing
from utilities.mistakes_corrector import mistakes_corrector
from utilities.multithreading import timee

bot = telebot.TeleBot('6573749748:AAHkgu9YEZrSoO4azALlhsJBOTpuQaciMwA')
# Функция для осуществления рассылки
def newsletter():
    signs = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы']
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
            photo = open(f'../signs_photo/{signs[user_id[1]-1]}.jpg', 'rb')
            bot.send_photo(user_id[0], photo)
            bot.send_message(user_id[0], horoscopes[user_id[1]])
            photo.close()
        except:
            logger.error("Не удается отправить сообщение пользователю в рассылке")
    connection.commit()
    connection.close()

# Массив с гороскопами
horoscopes = []
horoscope_parcing(horoscopes)
# Пока что парсинг и рассылка выполняется каждые 10 секунд, это сделано для простоты отладки функции подписки. 
# Интервал легко поменять на раз в день, немного подкорректировав две следующие функции
schedule.every(30).seconds.do(horoscope_parcing, horoscopes=[])
schedule.every(30).seconds.do(newsletter)
threading.Thread(target=timee).start()

# Нужно для клавиатуры в наталке
LSTEP = {'y': 'год рождения', 'm': 'месяц', 'd': 'день'}
# Запуск бота
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Натальная карта')
    btn2 = types.KeyboardButton('Совместимость')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Гороскоп на день')
    btn4 = types.KeyboardButton('Китайский знак зодиака')
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Что бы ты хотел узнать?', reply_markup=markup)

# Обработка запроса
@bot.message_handler(content_types=['text'])
def choose_option(message):
     #Начало
    if message.text.lower() == 'привет' or message.text.lower() == 'начало' or message.text.lower() == 'начать' or message.text.lower() == 'запуск':
        start(message)
    # Помощь
    elif message.text.lower() == '/help' or message.text.lower() == 'help' or message.text.lower() == 'помощь' or message.text.lower() == 'инфо' or message.text.lower() == 'информация':
        bot.send_message(message.chat.id,
                         '''С помощью этого бота ты можешь узнать свою натальную карту, совместимость или гороскоп. \n\nДля этого воспользуйся панелью управления снизу. \n\nПолный список команд можно увидеть,
нажав на кнопку "Меню" слева. \n\nНадеемся, наш бот тебе понравится:)''')
    # Натальная карта
    elif message.text.lower() == '/natal_chart' or message.text.lower() == 'натальная карта' or message.text.lower() == 'natal chart':
        calendar, step = DetailedTelegramCalendar(locale='ru').build()
        bot.send_message(message.chat.id,
                         f"Выберите {LSTEP[step]}",
                         reply_markup=calendar)
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
        bot.send_message(message.chat.id, 'Ты знаешь свой знак зодиака?', reply_markup=markup)
    # Китайский знак зодиака
    elif message.text.lower() == 'китайский знак' or message.text.lower() == 'китайский знак зодиака' or message.text.lower() == 'chinese_sign' or message.text.lower() == '/chinese_sign':
        bot.send_message(message.chat.id, 'Введи день, месяц и год рождения в формате: ДД.ММ.ГГГГ')
        bot.register_next_step_handler(message, chinese_sign_processing)
    # Знак зодиака
    elif message.text.lower() == 'знак' or message.text.lower() == 'sign' or message.text.lower() == '/sign':
        bot.send_message(message.chat.id, 'Введи день и месяц рождения в формате: ДД.ММ')
        bot.register_next_step_handler(message, date_to_sign_only)
    # Отписка от рассылки
    elif message.text.lower() == '/unsubscribe' or message.text.lower() == 'отписка':
        markup = types.InlineKeyboardMarkup()
        btn1 = (types.InlineKeyboardButton('Да', callback_data='unsyes'))
        btn2 = (types.InlineKeyboardButton('Нет', callback_data='unsno'))
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Ты уверен?', reply_markup=markup)
    # Смена знака гороскопа 
    elif message.text.lower() == '/change_sign':
        bot.send_message(message.chat.id, 'Введи новый знак зодиака для подписки')
        bot.register_next_step_handler(message, change_of_sign)
    # Чепуха
    else:
        bot.send_message(message.chat.id,
                         'К сожалению, я не умею выполнять эту команду:( Чтобы узнать, что я могу, введи команду /help')


#Функция для китайского знака гороскопа
def chinese_sign_processing(message):
    ans = chinese_sign(message.text)
    if ans == 0:
        bot.send_message(message.chat.id, 'Похоже, ты ввел дату в неправильном формате, попробуй еще раз')
        bot.register_next_step_handler(message, chinese_sign_processing)
    else:
        bot.send_message(message.chat.id, f'Твой знак зодиака: {ans}')


#Клавиатура в натальной карте
@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выберете {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}",
                              c.message.chat.id,
                              c.message.message_id)
        bot.send_message(c.message.chat.id, 'Введите время в формате HH:MМ. Если вы не знаете точное время рождения, введите 12:00.')
        bot.register_next_step_handler(c.message, natal_day, result)


# Функции для натальной карты
def natal_day(message, date):
    bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(message, natal_chart_processing, [date, message.text])


def natal_chart_processing(message, date):
    res = natal_chart(message.text, date)
    if res != 0:
        bot.send_message(message.chat.id, "Ваша натальная карта:")
        bot.send_message(message.chat.id, res)
        try:
            f = open("GFG-1.html", "rb")
            bot.send_message(message.chat.id, "Положение планет:")
            bot.send_document(chat_id=message.chat.id, document=f)
        except:
            logger.error('Проблемы с наталкой')
    else:
        bot.send_message(message.chat.id, "Не удалось составить натальную карту. Пожалуйста, попробуйте снова.")
        message.text = '/natal_chart'
        choose_option(message)


#Функция обработки запроса, когда пользователь просто хочет узнать свой знак
def date_to_sign_only(message):
    # Обработка запроса
    sign = date_to_sign(message.text)
    # Проверяем, нет ли ошибки
    if sign == -1:
        bot.send_message(message.chat.id, 'Похоже, ты ввел дату в неправильном формате, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_only)
    elif sign == 0:
        bot.send_message(message.chat.id, 'Не хватает разделителя между днем и месяцем, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_only)
    elif sign == 1:
        bot.send_message(message.chat.id, 'Что-то не так с месяцем, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_only)
    elif sign == 2:
        bot.send_message(message.chat.id, 'Введен неверный день, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_only)
    else:
        bot.send_message(message.chat.id, f'Твой знак зодиака: {sign}')
# Функция для обработки знает пользователь свой знак или нет
@bot.callback_query_handler(func=lambda callback: callback.data[0:4] == 'sign')
def processing_of_sign(callback):
    #Пользователь знает свой знак
    if callback.data[5:] == 'yes':
        #Для гороскопа
        if callback.data[4] == '1':
            mes = bot.send_message(callback.message.chat.id, 'Какой знак гороскопа тебя интереcует?')
            bot.register_next_step_handler(mes, mistakes_processing, 1)
        #Для совместимости
        else:
            mes = bot.send_message(callback.message.chat.id, 'Введи свой знак зодиака и знак зодиака своего партнера через пробел')
            bot.register_next_step_handler(mes, mistakes_processing, 2)
    #Не знает, переводим дату в знак
    else:
        if callback.data[4] == '1':
            mes = bot.send_message(callback.message.chat.id, 'Введи день и месяц рождения в формате: ДД.ММ')
            bot.register_next_step_handler(mes, date_to_sign_processing, 1)
        else:
            mes = bot.send_message(callback.message.chat.id, 'Введи свой день и месяц рождения в формате: ДД.ММ')
            bot.register_next_step_handler(mes, date_to_sign_processing, 2)
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


# Обработка случая, когда пользователь не знает знак
def date_to_sign_processing(message, k=0, two_signs=''):
    # Переводим дату в знак
    sign = date_to_sign(message.text)
    # Проверяем нет ли ошибки
    if sign == -1:
        bot.send_message(message.chat.id, 'Похоже, ты ввел дату в неправильном формате, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_processing, k, two_signs)
    elif sign == 0:
        bot.send_message(message.chat.id, 'Не хватает разделителя между днем и месяцем, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_processing, k, two_signs)
    elif sign == 1:
        bot.send_message(message.chat.id, 'Что-то не так с месяцем, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_processing, k, two_signs)
    elif sign == 2:
        bot.send_message(message.chat.id, 'Введен неверный день, попробуй еще раз')
        bot.register_next_step_handler(message, date_to_sign_processing, k, two_signs)
    else:
        # Случай гороскопа
        if k == 1 and two_signs == '':
            bot.send_message(message.chat.id, f'Твой знак зодиака: {sign}')
            res = horoscope_sign(sign)
            sign_of_user = horoscopes[res[1]]
            photo = open(f'../signs_photo/{res[0]}.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
            photo.close()
            bot.send_message(message.chat.id, sign_of_user)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data=f'subyes {res[1]}'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='subno'))
            bot.send_message(message.chat.id, 'Хочешь подписаться на ежедневную рассылку?', reply_markup=markup)
        #Для совместимости просто запускаем функцию два раза
        elif k == 2:
            bot.send_message(message.chat.id, f'Твой знак зодиака: {sign}')
            two_signs += sign
            k -= 1
            bot.send_message(message.chat.id, 'Введи день и месяц рождения своего партнера в формате: ДД.ММ')
            bot.register_next_step_handler(message, date_to_sign_processing, k, two_signs)
        else:
            bot.send_message(message.chat.id, f'Знак зодиака твоего партнера: {sign}')
            two_signs+= ' ' + sign
            message.text = two_signs
            # Спрашиваем пол
            gender_compatibility(message)

#Функция обработок ошибок в написании знака
def mistakes_processing(message, k):
    signs = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы']
    # Для гороскопа
    if k == 1:
        sign = message.text.lower()
        # Знак и так правильный
        if sign in signs:
            # Получаем гороскоп
            res = horoscope_sign(sign)
            sign_of_user = horoscopes[res[1]]
            photo = open(f'../signs_photo/{res[0]}.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
            photo.close()
            bot.send_message(message.chat.id, sign_of_user)
            # Предложение подписаться на рассылку
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data=f'subyes {res[1]}'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='subno'))
            bot.send_message(message.chat.id, 'Хочешь подписаться на ежедневную рассылку?', reply_markup=markup)
        # Все настолько плохо, что невозможно исправить
        elif len(sign) > 10 or len(sign) < 2:
            bot.send_message(message.chat.id, 'Такого знака нет:( Попробуй еще раз')
            bot.register_next_step_handler(message, mistakes_processing, 1)
        # Пробуем исправить
        else:
            corrected_sign = mistakes_corrector(sign)
            if corrected_sign == 0:
                bot.send_message(message.chat.id, 'Такого знака нет:( Попробуй еще раз')
                bot.register_next_step_handler(message, mistakes_processing, 1)
            # Уточняем, правильно ли мы исправили знак
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Да', callback_data=f'coryes1 {corrected_sign}'))
                markup.add(types.InlineKeyboardButton('Нет', callback_data='corno1'))
                bot.send_message(message.chat.id, f'Похоже, ты ошибся в знаке зодиака. Возможно ты имел в виду: {corrected_sign}', reply_markup=markup)
    #Случай для совместимости
    elif k == 2:
        two_signs = message.text.lower().split()
        if len(two_signs) != 2 or len(two_signs[0]) > 10 or len(two_signs[0]) < 2 or len(two_signs[1]) > 10 or len(two_signs[1]) < 2:
            bot.send_message(message.chat.id, 'Такого пары знаков нет:( Попробуй еще раз')
            bot.register_next_step_handler(message, mistakes_processing, 2)
        elif two_signs[0] in signs and two_signs[1] in signs:
            gender_compatibility(message)
        elif two_signs[0] in signs:
            corrected_sign = mistakes_corrector(two_signs[1])
            if corrected_sign == 0:
                bot.send_message(message.chat.id, 'Такого пары знаков нет:( Попробуй еще раз')
                bot.register_next_step_handler(message, mistakes_processing, 2)
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Да', callback_data=f'coryes2 {two_signs[0]} {corrected_sign}'))
                markup.add(types.InlineKeyboardButton('Нет', callback_data='corno2'))
                bot.send_message(message.chat.id, f'Похоже, ты ошибся в знаках зодиака. Возможно ты имел в виду: {two_signs[0]} {corrected_sign}', reply_markup=markup) 
        elif two_signs[1] in signs:
            corrected_sign = mistakes_corrector(two_signs[0])
            if corrected_sign == 0:
                bot.send_message(message.chat.id, 'Такой пары знаков нет:( Попробуй еще раз')
                bot.register_next_step_handler(message, mistakes_processing, 2)
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Да', callback_data=f'coryes2 {corrected_sign} {two_signs[1]}'))
                markup.add(types.InlineKeyboardButton('Нет', callback_data='corno2'))
                bot.send_message(message.chat.id, f'Похоже, ты ошибся в знаках зодиака. Возможно ты имел в виду: {corrected_sign} {two_signs[1]}', reply_markup=markup) 
        else:
            corrected_sign1 = mistakes_corrector(two_signs[0])
            corrected_sign2 = mistakes_corrector(two_signs[1])
            if corrected_sign1 == 0 or corrected_sign2 == 0:
                bot.send_message(message.chat.id, 'Такой пары знаков нет:( Попробуй еще раз')
                bot.register_next_step_handler(message, mistakes_processing, 2)
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Да', callback_data=f'coryes2 {corrected_sign1} {corrected_sign2}'))
                markup.add(types.InlineKeyboardButton('Нет', callback_data='corno2'))
                bot.send_message(message.chat.id, f'Похоже, ты ошибся в знаках зодиака. Возможно ты имел в виду: {corrected_sign1} {corrected_sign2}', reply_markup=markup) 


#Проверка правильно ли мы исправили знак
@bot.callback_query_handler(func=lambda callback: callback.data[0:3] == 'cor')
def mistakes_confirmation(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    #Исправили правильно
    if callback.data[3:6] == 'yes':
        if callback.data[6] == '1':
            callback.message.text = callback.data.split()[1]
            # Получаем гороскоп
            res = horoscope_sign(callback.message.text)
            sign_of_user = horoscopes[res[1]]
            photo = open(f'../signs_photo/{res[0]}.jpg', 'rb')
            bot.send_photo(callback.message.chat.id, photo)
            photo.close()
            bot.send_message(callback.message.chat.id, sign_of_user)
            #Предложение подписаться на рассылку
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data=f'subyes {res[1]}'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='subno'))
            bot.send_message(callback.message.chat.id, 'Хочешь подписаться на ежедневную рассылку?', reply_markup=markup)
        else:
            #Для совместимости переводим в выбор пола
            callback.message.text = callback.data[8:]
            gender_compatibility(callback.message)
    #Пользователь говорит, что исправили неправильно
    else:
        if callback.data[5] == '1':
            mes = bot.send_message(callback.message.chat.id, 'Пожалуйста, введи знак зодика еще раз')
            bot.register_next_step_handler(mes, mistakes_processing, 1)
        else:
            mes = bot.send_message(callback.message.chat.id, 'Пожалуйста, введи пару знаков зодика еще раз')
            bot.register_next_step_handler(mes, mistakes_processing, 2)

#Обработка пола для совместимости
def gender_compatibility(message):
    markup_syuy = types.InlineKeyboardMarkup()
    btn_syuy1 = (types.InlineKeyboardButton('👩', callback_data=f'sex_woman{message.text}'))
    btn_syuy2 = (types.InlineKeyboardButton('👨', callback_data=f'sex_man{message.text}'))
    markup_syuy.add(btn_syuy1, btn_syuy2)
    bot.send_message(message.chat.id, 'Выбери свой пол', reply_markup=markup_syuy)


#Обработка ответа на впорос о поле
@bot.callback_query_handler(func=lambda callback: callback.data[0:3] == 'sex')
def gender_processing(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    #Женщина
    if callback.data[4] == 'w':
        callback.message.text = callback.data[9:]
        mapa = compatibility(callback.message.text, 0)
    #Мужчина
    else:
        callback.message.text = callback.data[7:]
        mapa = compatibility(callback.message.text, 1)
    for x in mapa:
            bot.send_message(callback.message.chat.id, f'{x}\n')
            bot.send_message(callback.message.chat.id, f'{mapa[x]}\n\n')

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
            bot.send_message(callback.message.chat.id, 'У тебя и так нет подписки. Но мы можем это исправить:)')
        else:
            cursor.execute("DELETE FROM Users WHERE id=?", (user_id,))
            connection.commit()
            bot.send_message(callback.message.chat.id, 'Подписка отменена')
        connection.close()       
    else:
        bot.send_message(callback.message.chat.id, 'Рад, что ты решил не отписываться')
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


bot.polling(none_stop=True)
