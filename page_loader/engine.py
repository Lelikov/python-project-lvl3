import os
import re
from urllib.parse import urlparse, urlunparse
import requests
from bs4 import BeautifulSoup
import logging
import sys
from progress.bar import Bar

REGEX = r'[^A-Za-z0-9]'
EXT = '.html'
SCHEME = 'http'
POSTFIX = '_files/'
ATTRIBUTES = ['src', 'href']

logging.basicConfig(filemode='w',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename='page_loader.log',
                    format='[%(asctime)s] %(module)s - %(levelname)s - %(message)s',
                    )
logger = logging.getLogger()

console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.WARNING)
logger.addHandler(console_handler)


def loader(url, output, log):
    logger.setLevel(log.upper())

    url, output = arguments_normalization(url, output)
    changed_url = change_url(url)

    try:
        get_page = requests.get(url)
        get_page.raise_for_status()
        page = BeautifulSoup(get_page.text, "html.parser")
    except requests.exceptions.RequestException as error:
        logger.critical(error)
        return 11

    folder = os.path.join(output, changed_url + POSTFIX)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            logger.warning('Created folder {}'.format(folder))
        except OSError as error:
            logger.critical(error)
            return 21

    bar = create_bar(page)

    for attribute in ATTRIBUTES:
        param = {attribute: True}
        for tag in page.find_all(**param):
            normalized_url = url_normalization(tag[attribute], url)
            logger.debug('{} normalized to {}'.format(tag[attribute], normalized_url))

            if tag.name == 'a':
                tag[attribute] = normalized_url
            else:
                tag[attribute] = download_file(normalized_url, folder, changed_url)

            logger.debug('New {} is {}'.format(attribute, tag[attribute]))
            bar.next()

    logger.info('Downloading completed')
    bar.finish()

    try:
        with open(os.path.join(output, changed_url + EXT), 'w') as path:
            path.write(page.prettify())
            logger.info('Modified page created')
    except OSError as error:
        logger.critical(error)
        return 22
    return 0


def download_file(normalized_url, folder, changed_url):
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
        return 12
    file = get_file.content
    logger.debug('{} is downloaded'.format(normalized_url))

    file_path = os.path.join(folder, changed_filename + file_extension)

    try:
        with open(file_path, 'wb') as received_file:
            received_file.write(file)
            logger.debug('{} is created'.format(file_path))
    except OSError as error:
        logger.critical(error)
        return 23

    return changed_url + POSTFIX + changed_filename + file_extension


def arguments_normalization(url, output):
    if url.endswith('/'):
        url = url[:-1]
        logger.warning('Deleted last / in the URL')
    if not urlparse(url).scheme:
        url = urlunparse((SCHEME, url, '', '', '', ''))
        logger.warning('URL was changed. Added {}://'.format(SCHEME))
    if not output.endswith('/'):
        output = os.path.join(output, '')
        logger.warning('Added / to the end of output')
    return url, output


def create_bar(page):
    max_bar = 0
    for attribute in ATTRIBUTES:
        param = {attribute: True}
        max_bar += len(page.find_all(**param))
    logger.debug('Generated {} steps for progress bar'.format(max_bar))
    return Bar('Progress', max=max_bar)


def change_url(old_url):
    parsed_url = urlparse(old_url)
    changed_url = re.sub(REGEX, '-', parsed_url.netloc + parsed_url.path)
    logger.debug('{} changed to {}'.format(old_url, changed_url))
    return changed_url


def url_normalization(path, url):
    parsed_url = urlparse(path)
    if parsed_url.scheme:
        return path
    elif parsed_url.netloc:
        logger.debug('Added {}: to {}'.format(SCHEME, path))
        return urlunparse((SCHEME, parsed_url.netloc, parsed_url.path, '', '', ''))
    elif parsed_url.path.startswith('/'):
        logger.debug('Added {} to {}'.format(url, path))
        return urlunparse((SCHEME, urlparse(url).netloc, parsed_url.path, '', '', ''))
    logger.debug('Added {}/ to {}'.format(url, path))
    return urlunparse((SCHEME, urlparse(url).netloc, urlparse(url).path + '/' + path, '', '', ''))

# def test():
#     sys.exit(loader('localhost/test/qw', '/Users/alexandrlelikov/Desktop/Python', 'debug'))
#
#
# test()
