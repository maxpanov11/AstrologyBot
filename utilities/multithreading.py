# Разделение потоков, чтобы парсинг, рассылка и основной функционал бота могли работать вместе
import time

import schedule


def timee():
    while True:
        schedule.run_pending()
        time.sleep(1)
