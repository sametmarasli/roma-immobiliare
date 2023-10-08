import logging
from src import LOG_PATH

formatter = "%(asctime)s - %(levelname)s : %(message)s"
logging.basicConfig(filename=LOG_PATH, encoding='utf-8', filemode ='a', level=logging.INFO, format=formatter, datefmt = "%Y-%m-%d %H:%M:%S")

def info(message):
    logging.info(message)

def error(message):
    logging.error(message)