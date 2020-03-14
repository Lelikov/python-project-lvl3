import os

from page_loader.constants import ATTRIBUTES, EXT, POSTFIX
from page_loader.creators import (create_directory, create_page,
                                  create_progress_bar)
from page_loader.getters import get_file, get_page
from page_loader.logger import logger
from page_loader.normalizers import (arguments_normalization, change_symbols,
                                     url_normalization)


def loader(url, output, log):
    '''
    Download web page
    :param url: Web page URL
    :param output: Directory for save
    :param log: Logging level
    :return: None
    '''
    logger.setLevel(log.upper())

    url, output = arguments_normalization(url, output)
    page = get_page(url)
    changed_url = change_symbols(url)
    folder = os.path.join(output, changed_url + POSTFIX)
    if not os.path.exists(folder):
        create_directory(folder)
    bar = create_progress_bar(page)

    for attribute in ATTRIBUTES:
        param = {attribute: True}
        for tag in page.find_all(**param):
            normalized_url = url_normalization(tag[attribute], url)
            logger.debug('{} normalized to {}'.format(tag[attribute], normalized_url))
            if tag.name == 'a':
                tag[attribute] = normalized_url
            else:
                tag[attribute] = get_file(normalized_url, folder, changed_url)
            logger.debug('New {} is {}'.format(attribute, tag[attribute]))
            bar.next()

    logger.info('Downloading completed')
    create_page(os.path.join(output, changed_url + EXT), page)
    bar.finish()
    return
