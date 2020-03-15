import os

from progress.bar import Bar

from page_loader.constants import ATTRIBUTES
from page_loader.logger import logger


def save_page(path, page):
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


def save_file(file_path, file):
    '''
    Save file from request
    :param file_path: Path to new file
    :param file: File from request
    :return: None
    '''
    try:
        with open(file_path, 'wb') as received_file:
            received_file.write(file)
            logger.debug('{} is created'.format(file_path))
    except OSError as error:
        logger.critical(error)
        raise OSError(5)


def loading_progress(max_bar):
    '''
    Created progress bar
    :param max_bar: Max progress bar steps
    :return: progress.bar object
    '''
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
        raise OSError('Failed to make directory')


def create_tag_list(page):
    '''
    Create list of tags from page
    :param page: bs4.BeautifulSoup class
    :return: List of tags
    '''
    tag_list = []
    for attribute in ATTRIBUTES:
        param = {attribute: True}
        for tag in page.find_all(**param):
            tag_list.append(tag)
    return tag_list
