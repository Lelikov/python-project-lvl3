import os
from page_loader.normalizers import arguments_normalization, url_normalization, change_url
from page_loader.creators import create_page, create_directory, create_progress_bar
from page_loader.constants import POSTFIX, ATTRIBUTES, EXT
from page_loader.getters import get_page, get_file
from page_loader.logger import logger


def loader(url, output, log):
    logger.setLevel(log.upper())

    url, output = arguments_normalization(url, output)
    page = get_page(url)
    changed_url = change_url(url)
    folder = os.path.join(output, changed_url + POSTFIX)
    if not os.path.exists(folder):
        create_directory(folder)
    bar = create_progress_bar(page)
    change_attribute(page, url, folder, changed_url, bar)
    logger.info('Downloading completed')
    create_page(os.path.join(output, changed_url + EXT), page)
    bar.finish()
    return


def change_attribute(page, url, folder, changed_url, bar):
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
    return
