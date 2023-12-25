import base64
import datetime
import json

import json2html
import requests

from utilities.logger import logger


def natal_chart(city, date):
    try:

        birth_date = date[0]  # Date format: DD:MM:YYYY
        birth_time = date[1]  # Time format: HH:MM
        birth_time1 = birth_time.split(':')
        if len(birth_time1) != 2 or len(birth_time) != 5 or int(birth_time1[0]) > 23 or int(birth_time1[1]) > 59:
                return 0

        parsed_date = birth_date.strftime("%d:%m:%Y") + " " + birth_time

        # Создание нового объекта datetime с нужной датой (2000-01-01) и временем (00:00:00)
        new_date = datetime.datetime(2000, 1, 1)
        # Конечный формат даты и времени
        formatted_date = new_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        # Конечная точка API и параметры для создания натальной карты
        api_endpoint = 'https://json.astrologyapi.com/v1/western_horoscope'
        api_endpoint2 = 'https://json.astrologyapi.com/v1/natal_wheel_chart'
        api_key = '4376aed766820ab11e327c11d76be824'

        # Сделать запрос к API
        response = requests.post(api_endpoint, json={"year" : int(parsed_date[6:10]),
                                                     "month" : int(parsed_date[3:5]),
                                                     "day" : int(parsed_date[0:2]),
                                                     "hour": int(parsed_date[11:13]),
                                                     "min" : int(parsed_date[14:]),
                                                     "lat": 50.8476424,
                                                     "lon": 4.3571696,
                                                     "tzone" : 5
                                                     }, headers = {"Content-Type":'application/json', "authorization": "Basic " + base64.b64encode(("627384" + ":" + api_key).encode()).decode()})

        response2 = requests.post(api_endpoint2, json={"year" : int(parsed_date[6:10]),
                                                     "month" : int(parsed_date[3:5]),
                                                     "day" : int(parsed_date[0:2]),
                                                     "hour": int(parsed_date[11:13]),
                                                     "min" : int(parsed_date[14:]),
                                                     "lat": 50.8476424,
                                                     "lon": 4.3571696,
                                                     "tzone" : 5
                                                     }, headers = {"Content-Type":'application/json', "authorization": "Basic " + base64.b64encode(("627384" + ":" + api_key).encode()).decode()})
        if response.status_code == 200 and response2.status_code == 200:
            dict = json.loads(response2.text)
            natal_chart = response.json()  # Предполагаем, что API возвращает данные в формате JSON
            html = json2html.json2html.convert(json=natal_chart)
            htmlFile = open("GFG-1.html", "w")
            htmlFile.write(html)
            htmlFile.close()
            return dict["chart_url"]       
    except:
        logger.info('Не получилось выдать наталку')
        return 0
