import requests
from bs4 import BeautifulSoup

from utilities.logger import logger


def chinese_sign(date):
    signs = ['Обезьяна', 'Петух', 'Собака', 'Свинья', 'Крыса', 'Бык', 'Тигр', 'Кролик', 'Дракон', 'Змея', 'Лошадь', 'Овца']
    try:
        day, month, year = date.split('.')
    except:
        logger.info("Что-то не так с вводом в китае")
        return 0
    if len(year) != 4 or len(month) != 2 or len(day) != 2 or int(year) < 1900 or int(year) > 2023 or int(month) > 12 or int(day) > 31:
        return 0
    if month != '01' and month != '02':
        sign = signs[int(year) % 12]
        return sign
    else:
        response = requests.get('http://www.astronet.ru/db/msg/1196222').text
        soup = BeautifulSoup(response, 'lxml')
        block = soup.find_all('td')
        flag = 0
        flag2 = 0
        res = ''
        for s in block:
            for k in s.stripped_strings:
                if k == year:
                    flag = 1
                elif flag == 1 and (k[0:3] == 'янв' or k[0:3] == 'фев'):
                    res = k
                    flag2 = 1
                    break
            if flag2 == 1:
                break
        res = res.split()
        if res[0] == 'янв':
            res[0] = 1
        else:
            res[0] = 2
        res[1] = int(res[1])
        month = int(month)
        day = int(day)
        if month > res[0] or (month == res[0] and day >= res[1]):
            sign = signs[int(year) % 12]
        else:
            sign = signs[(int(year)-1) % 12]
        return sign
