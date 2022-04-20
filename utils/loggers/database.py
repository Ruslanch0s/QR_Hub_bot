import logging
from logging.handlers import RotatingFileHandler  # следит за храниением лог файлов


logger = logging.getLogger(__name__)  # отдельный логгер для работы с бд
logger.setLevel(logging.INFO)  # установка уровня (error, info и тд)

handler = RotatingFileHandler('loggs/database_status.log', maxBytes=50000000, backupCount=5)  # папка с логами, max вес файла, макс кол-во файлов этого лога (старые удаляются)
formatter = logging.Formatter('%(message)s - %(asctime)s - %(lineno)s')  # message - текст ошибки, asctime - время события, lineno - номер строки)))
handler.setFormatter(formatter)  # форматер дополняет логгирование (помимо message есть куча всего)
logger.addHandler(handler)  # к глобальному хендлеру добавляется локальный

