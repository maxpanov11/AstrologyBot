# парсинг совместимости
def compatibility_parcing(merged_collection):
    URL = 'https://www.nur.kz/esoterics/astrology/1824471-lubov-znakov-zodiaka-kak-lubit-kazdyj-znak/'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    collection = soup.find_all('p', class_="align-left formatted-body__paragraph")[1:-1]
    for i in range(1, len(collection), 2):
        merged_collection.append(collection[i - 1].text + collection[i].text)


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
        # Пробуем исправить ошибки в неверно введенном знаке
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
