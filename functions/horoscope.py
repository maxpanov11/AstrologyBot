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


# Функция для отправки гороскопа
def horoscope_sign(message):
    map_sign = {'овен': 1, 'телец': 2, 'близнецы': 3, 'рак': 4, 'лев': 5, 'дева': 6, 'весы': 7, 'скорпион': 8, 'стрелец': 9, 'козерог': 10, 'водолей': 11, 'рыбы': 12}
    sign_of_user = map_sign.get(message.text.lower(), 0)
    cnt = 0
    if sign_of_user != 0:
        bot.send_message(message.chat.id, horoscopes[sign_of_user])
    else:
        # Пробуем исправить ошибки в неверно введенном знаке
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

        
# Функция оформления подписки
@bot.callback_query_handler(func=lambda callback: True)
def subscription(callback):
    if callback.data[0:3] == 'yes':
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


# Функция отписки от рассылки
def unsubscribe(message):
    if message.text.lower() == 'да' or message.text.lower() == 'yes' or message.text.lower() == 'уверен':
        connection = sqlite3.connect('my_database5.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER,
        sign INTEGER
        )
        ''')
        exist = cursor.execute('SELECT * FROM Users where id=?', (message.chat.id,))
        if exist.fetchone() is None:
            bot.send_message(message.chat.id, 'У тебя и так нет подписки')
        else:
            cursor.execute("DELETE FROM Users WHERE id=?", (message.chat.id,))
            connection.commit()
            bot.send_message(message.chat.id, 'Подписка отменена')
        connection.close()       
    else:
        bot.send_message(message.chat.id, 'Рад, что ты решил не отписываться')
    bot.register_next_step_handler(message, choose_option)


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
