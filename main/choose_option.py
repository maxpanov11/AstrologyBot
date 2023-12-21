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
