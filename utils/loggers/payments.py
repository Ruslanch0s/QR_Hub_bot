import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler('loggs/payments_status.log', maxBytes=50000000, backupCount=5)
formatter = logging.Formatter('%(message)s - %(asctime)s - %(lineno)s')
handler.setFormatter(formatter)
logger.addHandler(handler)