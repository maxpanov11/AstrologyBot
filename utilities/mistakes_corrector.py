# Функция обработок ошибок в написании знака c помощью расстояния Левенштейна
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


# Функция процессинга для функции обработки ошибок
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
