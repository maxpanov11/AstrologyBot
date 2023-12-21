# Разделение потоков, чтобы парсинг, рассылка и основной функционал бота могли работать вместе
def timee():
    while True:
        schedule.run_pending()
        time.sleep(1)
