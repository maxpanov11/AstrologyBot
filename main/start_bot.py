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

# Массив с гороскопами
horoscopes = []
horoscope_parcing(horoscopes)

# Массив с совместимостью
merged_collection = []
compatibility_parcing(merged_collection)

# Запуск многопоточности
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

