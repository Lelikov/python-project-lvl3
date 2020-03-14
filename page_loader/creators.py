import os

from progress.bar import Bar

from page_loader.constants import ATTRIBUTES
from page_loader.logger import logger


def create_page(path, page):
    '''
    Created page from BeautifulSoup object
    :param path: Destination directory
    :param page: BeautifulSoup object
    :return: None
    '''
    try:
        with open(path, 'w') as file:
            file.write(page.prettify())
            logger.info('Modified page created')
    except OSError as error:
        logger.critical(error)
        raise OSError(6)


def create_progress_bar(page):
    '''
    Created progress bar
    :param page: BeautifulSoup object for count max progress bar steps
    :return: progress.bar object
    '''
    max_bar = 0
    for attribute in ATTRIBUTES:
        param = {attribute: True}
        max_bar += len(page.find_all(**param))
    logger.debug('Generated {} steps for progress bar'.format(max_bar))
    return Bar('Progress', max=max_bar)


def create_directory(folder):
    '''
    Create directory
    :param folder: Path to folder
    :return:
    '''
    try:
        os.makedirs(folder)
        logger.warning('Created folder {}'.format(folder))
    except OSError as error:
        logger.critical(error)
        raise OSError(4)
