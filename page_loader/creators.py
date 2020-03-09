from page_loader.constants import ATTRIBUTES
from page_loader.logger import logger
from progress.bar import Bar
import os


def create_page(path, page):
    try:
        with open(path, 'w') as file:
            file.write(page.prettify())
            logger.info('Modified page created')
    except OSError as error:
        logger.critical(error)
        raise OSError(6)


def create_progress_bar(page):
    max_bar = 0
    for attribute in ATTRIBUTES:
        param = {attribute: True}
        max_bar += len(page.find_all(**param))
    logger.debug('Generated {} steps for progress bar'.format(max_bar))
    return Bar('Progress', max=max_bar)


def create_directory(folder):
    try:
        os.makedirs(folder)
        logger.warning('Created folder {}'.format(folder))
    except OSError as error:
        logger.critical(error)
        raise OSError(4)
