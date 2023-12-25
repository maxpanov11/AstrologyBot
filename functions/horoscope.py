# Функция для отправки гороскопа


def horoscope_sign(sign):
    map_sign = {'овен': 1, 'телец': 2, 'близнецы': 3, 'рак': 4, 'лев': 5, 'дева': 6, 'весы': 7, 'скорпион': 8, 'стрелец': 9, 'козерог': 10, 'водолей': 11, 'рыбы': 12}
    sign_of_user = map_sign.get(sign.lower(), 0)
    return [sign.lower(), sign_of_user]
