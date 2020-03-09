import requests
from bs4 import BeautifulSoup
from page_loader.normalizers import change_url
from page_loader.logger import logger
from page_loader.constants import POSTFIX
import os


def get_page(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
        return BeautifulSoup(page.text, "html.parser")
    except requests.exceptions.RequestException as error:
        logger.critical(error)
        raise requests.exceptions.RequestException(2)


def get_file(normalized_url, folder, changed_url):
    filename, file_extension = os.path.splitext(normalized_url)

    if filename.startswith('data:'):
        return normalized_url

    changed_filename = change_url(filename)
    logger.debug('New filename for {}{} is {}{}'.format(filename, file_extension,
                                                        changed_filename,
                                                        file_extension))
    try:
        get_file = requests.get(normalized_url)
        get_file.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.critical(error)
        raise requests.exceptions.RequestException(3)
    file = get_file.content
    logger.debug('{} is downloaded'.format(normalized_url))

    file_path = os.path.join(folder, changed_filename + file_extension)

    try:
        with open(file_path, 'wb') as received_file:
            received_file.write(file)
            logger.debug('{} is created'.format(file_path))
    except OSError as error:
        logger.critical(error)
        raise OSError(5)

    return changed_url + POSTFIX + changed_filename + file_extension
