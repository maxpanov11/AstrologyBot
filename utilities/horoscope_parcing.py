# Функция для парсинга гороскопов
import requests
from bs4 import BeautifulSoup

from utilities.logger import logger


def horoscope_parcing(horoscopes):
    try:
        link = 'https://retrofm.ru/goroskop'
        response = requests.get(link).text
        soup = BeautifulSoup(response, 'lxml')
        block = soup.find('div', id='all_wrapper')
        horoscope_block = block.find('div', class_='horoscope_list')
        horoscope_list = horoscope_block.find_all('div', class_='text_box')
        for predict in horoscope_list:
            horoscopes.append(predict.text)
    except:
        logger.critical('Упал парсинг горосокопов')
