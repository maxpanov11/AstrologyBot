import requests
from bs4 import BeautifulSoup

from utilities.logger import logger


# Функция для совместимости
def compatibility(two_signs, gender = 0):
    try:
        mass = two_signs.lower().split()
        mass[1] = mass[1].capitalize()
        URL = 'https://horo.mail.ru/compatibility/zodiac/'
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        collection = soup.find_all('a', class_="link link_block margin_top_10")
        first = mass[0]
        second = mass[1]
        if gender == 0:
            first_sign = 'Женщина-' + f'{first}'
            second_sign = 'мужчина ' + f'{second}'
        else:
            first_sign = 'Мужчина-' + f'{first}'
            second_sign = 'женщина ' + f'{second}'
        first_href = ''
        second_href = ''
        for i in collection:
            i = str(i)
            x = i.find(first_sign)
            if x != -1:
                index_of_first_href = i.find("href")
                first_href = i[index_of_first_href:][5:]
                index_span = first_href.find("<span")
                first_href = first_href[1:index_span - 2]
        lol = 'https://horo.mail.ru'
        URL1 = 'https://horo.mail.ru' + first_href
        r1 = requests.get(URL1)
        soup1 = BeautifulSoup(r1.text, 'html.parser')
        collection1 = soup1.find_all('a', class_="hdr__text")
        for j in collection1:
            j = str(j)
            y = j.find(second_sign)
            if y != -1:
                href_start = j.find("href=")
                href_end = j.find("><span")
                second_href = j[href_start + 6: href_end - 1]
        final_URL = lol + second_href
        r2 = requests.get(final_URL)
        soup = BeautifulSoup(r2.text, 'html.parser')
        collection2 = soup.find_all('h2')  # , class_="link link_block margin_top_10")
        collection2_more = soup.find_all('p')  # , class_="link link_block margin_top_10")
        mapa = {}
        for i in range(len(collection2)):
            x = str(collection2[i])
            begin = x.find("<h2>")
            end = x.find("</h2>")
            x = x[begin + 4: end]
            collection2[i] = x

        for j in range(len(collection2_more)):
            x = str(collection2_more[j])
            begin = x.find("<p>")
            end = x.find("</p>")
            x = x[begin + 3: end]
            collection2_more[j] = x

        for k in range(len(collection2)):
            mapa[collection2[k]] = collection2_more[k]
        # выдача совместимости
        return mapa
    except:
        logger.critical('Упал парсинг совместимости')
