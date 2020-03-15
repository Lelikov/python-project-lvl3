import os

import requests
from bs4 import BeautifulSoup

from page_loader.constants import POSTFIX, ATTRIBUTES
from page_loader.creators import save_file
from page_loader.logger import logger
from page_loader.normalizers import change_symbols


def get_page(url):
    '''
    Download page
    :param url: URL
    :return: BeautifulSoup object
    '''
    try:
        page = requests.get(url)
        page.raise_for_status()
        return BeautifulSoup(page.text, "html.parser")
    except requests.exceptions.RequestException as error:
        logger.critical(error)
        raise requests.exceptions.RequestException(2)


def get_file(normalized_url, folder, changed_url):
    '''
    Download file
    :param normalized_url: URL for downloads
    :param folder: Destination folder
    :param changed_url: File name
    :return: Path to downloaded file
    '''
    filename, file_extension = os.path.splitext(normalized_url)

    if filename.startswith('data:'):
        return normalized_url

    changed_filename = change_symbols(filename)
    logger.debug('New filename for {}{} is {}{}'.format(filename, file_extension,
                                                        changed_filename,
                                                        file_extension))
    try:
        get_files = requests.get(normalized_url)
        get_files.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.critical(error)
        raise requests.exceptions.RequestException(3)
    file = get_files.content
    logger.debug('{} is downloaded'.format(normalized_url))

    file_path = os.path.join(folder, changed_filename + file_extension)
    save_file(file_path, file)
    return os.path.join(changed_url + POSTFIX, changed_filename + file_extension)


def get_attribute(tag, n=0):
    if tag.get(ATTRIBUTES[n]) is None:
        return get_attribute(tag, n + 1)
    return ATTRIBUTES[n]
