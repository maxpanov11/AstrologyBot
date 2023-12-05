import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('6573749748:AAHkgu9YEZrSoO4azALlhsJBOTpuQaciMwA')


#Запуск бота
@bot.message_handler()
def start(message):
    if message.text.lower() == '/start' or message.text.lower() == 'привет' or message.text.lower() == 'начало' or message.text.lower() == 'начать' or message.text.lower() == 'запуск':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Натальная карта')
        btn2 = types.KeyboardButton('Совместимость')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Гороскоп на день')
        markup.row(btn3)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Что бы ты хотел узнать?', reply_markup=markup)
        bot.register_next_step_handler(message, choose_option)
#Обработка запроса пользователя
def choose_option(message):
    #Если нужна помощь
    if message.text.lower() == '/help' or message.text.lower() == 'help' or message.text.lower() == 'помощь' or message.text.lower() == 'инфо' or message.text.lower() == 'информация':
        bot.send_message(message.chat.id, 'С помощью этого бота ты можешь узнать свою натальную карту, совместимость или гороскоп. Для этого воспользуйся панелью управления снизу. Надеемся, наш бот тебе понравится:)')
        bot.register_next_step_handler(message, choose_option)
    #Натальная карта
    elif message.text.lower() == '/natal_chart' or message.text.lower() == 'натальная карта' or  message.text.lower() == 'natal chart':
        bot.send_message(message.chat.id, 'Извини, эта функция появится позже')
        bot.register_next_step_handler(message, choose_option)
    #Совместимость
    elif message.text.lower() == 'совместимость' or message.text.lower() == '/compatibility' or  message.text.lower() == 'compatibility':
        bot.send_message(message.chat.id, 'Извини, эта функция появится позже')
        bot.register_next_step_handler(message, choose_option)
    #Гороскоп
    elif message.text.lower() == 'гороскоп' or message.text.lower() == 'horoscope' or message.text.lower() == '/daily_horoscope'  or message.text.lower() == 'гороскоп на день' or message.text.lower() == 'daily_horoscope':
        bot.send_message(message.chat.id, 'Какой знак гороскопа тебя интереcует?')
        bot.register_next_step_handler(message, horoscope_sign)
    #Чепуха
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не умею выполнять эту команду:( Чтобы узнать, что я могу, введи команду /help')
        bot.register_next_step_handler(message, choose_option)
#Функция для натальной карты
def natal_chart(message):
    pass
#Функция для совместимости
def compatibility(message):
    pass
#Функция для парсинга и отправки гороскопа
def horoscope_sign(message):
    link = 'https://retrofm.ru/goroskop'
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'lxml')
    block = soup.find('div', id = 'all_wrapper')
    horoscope_block = block.find('div', class_ = 'horoscope_list')
    horoscope_list = horoscope_block.find_all('div', class_ = 'text_box')
    horoscopes = []
    cnt = 0
    for predict in horoscope_list:
        horoscopes.append(predict.text)
    if message.text.lower() == 'овен':
        bot.send_message(message.chat.id, horoscopes[1])
    elif message.text.lower() == 'телец':
        bot.send_message(message.chat.id, horoscopes[2])
    elif message.text.lower() == 'близнецы':
        bot.send_message(message.chat.id, horoscopes[3])
    elif message.text.lower() == 'рак':
        bot.send_message(message.chat.id, horoscopes[4])
    elif message.text.lower() == 'лев':
        bot.send_message(message.chat.id, horoscopes[5])
    elif message.text.lower() == 'дева':
        bot.send_message(message.chat.id, horoscopes[6])
    elif message.text.lower() == 'весы':
        bot.send_message(message.chat.id, horoscopes[7])
    elif message.text.lower() == 'скорпион':
        bot.send_message(message.chat.id, horoscopes[8])
    elif message.text.lower() == 'стрелец':
        bot.send_message(message.chat.id, horoscopes[9])
    elif message.text.lower() == 'козерог':
        bot.send_message(message.chat.id, horoscopes[10])
    elif message.text.lower() == 'водолей':
        bot.send_message(message.chat.id, horoscopes[11])
    elif message.text.lower() == 'рыбы':
        bot.send_message(message.chat.id, horoscopes[12])
    else:
        bot.send_message(message.chat.id, 'Такого знака нет:( Попробуй еще раз')
        bot.register_next_step_handler(message, horoscope_sign)
        cnt = 1
    if cnt == 0:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='yes'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='no'))
        bot.send_message(message.chat.id, 'Хочешь подписаться на ежедневную рассылку?', reply_markup=markup)
    if cnt == 0:
        bot.register_next_step_handler(message, choose_option)
#Функция для подписки на гороскоп
@bot.callback_query_handler(func=lambda callback: True)
def subscription(callback):
    if callback.data == 'yes':
        bot.send_message(callback.message.chat.id, 'Подписка успешно оформлена')
    else:
        bot.send_message(callback.message.chat.id, 'Очень жаль, что ты не хочешь оформить подписку. Надеемся, ты передумаешь')
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
bot.polling(none_stop=True)
