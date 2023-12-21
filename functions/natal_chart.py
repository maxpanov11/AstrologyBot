# Функция для натальной карты
def natal_chart(message):
    user_input = message.text.split()

    if len(user_input) < 3:
        bot.reply_to(message, "Пожалуйста, укажите дату, время и место (город) в правильном формате.")
        return

    birth_date = user_input[0]  # Date format: DD:MM:YYYY
    birth_time = user_input[1]  # Time format: HH:MM

    parsed_date = datetime.datetime.strptime(birth_date + " " + birth_time, "%d:%m:%Y %H:%M")

    # Создание нового объекта datetime с нужной датой (2000-01-01) и временем (00:00:00)
    new_date = datetime.datetime(2000, 1, 1)
    # Конечный формат даты и времени
    formatted_date = new_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # Конечная точка API и параметры для создания натальной карты
    api_endpoint = 'https://api.astroapi.cloud/horoscope/natal/calculate'
    api_key = 'MndMdGc4by9RWlN1RVFlcSsrQXVDdz09Lit5c3lXbGdDVHF1aU1qalcxSFJLNmc9PQ=='

    # Сделать запрос к API
    response = requests.post(api_endpoint, json={"dateTime": formatted_date,
                                                 "latitude": 50.8476424,
                                                 "longitude": 4.3571696}, headers={'X-Api-Key': api_key})

    if response.status_code == 200:
        natal_chart = response.json()  # Предполагаем, что API возвращает данные в формате JSON
        html = json2html.json2html.convert(json=natal_chart)
        htmlFile = open("GFG-1.html", "w")
        htmlFile.write(html)
        htmlFile.close()

        f = open("GFG-1.html", "rb")

        bot.send_document(chat_id=message.chat.id, document=f)
        bot.register_next_step_handler(message, choose_option)

    else:
        bot.reply_to(message, "Не удалось составить натальную карту. Пожалуйста, попробуйте снова.")

