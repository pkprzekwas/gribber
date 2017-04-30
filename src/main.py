import time
import os

from logger import logger
from crawler import Crawler


def main():
    logger.info('Starting...')
    c = Crawler()
    c.start()
    logger.info('Finished.')


if __name__ == '__main__':
    main()