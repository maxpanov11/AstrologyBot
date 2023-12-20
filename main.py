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
                         'С помощью этого бота ты можешь узнать свою натальную карту, совместимость или гороскоп. Для этого воспользуйся панелью управления снизу. Надеемся, наш бот тебе понравится:)')
        bot.register_next_step_handler(message, choose_option)
    # Натальная карта
    elif message.text.lower() == '/natal_chart' or message.text.lower() == 'натальная карта' or message.text.lower() == 'natal chart':
        bot.send_message(message.chat.id, 'Введите время в формате DD:MM:YYYY HH:MM и город')
        bot.register_next_step_handler(message, natal_chart)
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
    # Смена знака гороскопа 
    elif message.text.lower() == '/change_sign':
        bot.send_message(message.chat.id, 'Введи новый знак зодиака для подписки')
        bot.register_next_step_handler(message, change_of_sign)
    # Чепуха
    else:
        bot.send_message(message.chat.id,
                         'К сожалению, я не умею выполнять эту команду:( Чтобы узнать, что я могу, введи команду /help')
        bot.register_next_step_handler(message, choose_option)
