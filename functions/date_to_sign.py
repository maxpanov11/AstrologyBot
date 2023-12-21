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
