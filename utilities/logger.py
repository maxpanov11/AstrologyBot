import logging

logger = logging.getLogger("parcing_and_messsages")
logger.setLevel(logging.INFO)
handler_for_exceptions = logging.FileHandler("logging_file.log", mode='w')
logger.addHandler(handler_for_exceptions) # добавление handler'a в логгер