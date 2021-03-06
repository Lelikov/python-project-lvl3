import os

from page_loader.constants import EXT, POSTFIX, ATTRIBUTES
from page_loader.creators import (create_directory, create_tag_list,
                                  loading_progress, save_page)
from page_loader.getters import get_file, get_page
from page_loader.logger import logger
from page_loader.normalizers import (arguments_normalization, change_symbols,
                                     url_normalization)


def loader(url, output):
    '''
    Download web page
    :param url: Web page URL
    :param output: Directory for save
    :param log: Logging level
    :return: None
    '''

    url, output = arguments_normalization(url, output)
    page = get_page(url)
    changed_url = change_symbols(url)
    folder = os.path.join(output, changed_url + POSTFIX)
    if not os.path.exists(folder):
        create_directory(folder)
    tag_list = create_tag_list(page)

    with loading_progress(len(tag_list)) as progress:
        for tag in tag_list:
            attribute = list(filter(lambda x: x is not None, map(tag.get, ATTRIBUTES)))[0]
            normalized_url = url_normalization(attribute, url)
            logger.debug('{} normalized to {}'.format(attribute, normalized_url))
            if tag.name == 'a':
                attribute = normalized_url
            else:
                attribute = get_file(normalized_url, folder, changed_url)
            logger.debug('New {} is {}'.format(attribute, attribute))
            progress.next()

    logger.info('Downloading completed')
    save_page(os.path.join(output, changed_url + EXT), page)
