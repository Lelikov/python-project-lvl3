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

    if url.endswith('/'):
        url = url[:-1]
        logger.warning('Deleted last / in the URL')
    elif not urlparse(url).scheme:
        url = urlunparse((SCHEME, url, '', '', '', ''))
        logger.warning('URL was changed. Added http://')
    elif not output.endswith('/'):
        output = os.path.join(output, '')
        logger.warning('Added / to the end of output')

    changed_url = change_url(url)

    try:
        get_page = requests.get(url)
        get_page.raise_for_status()
        page = BeautifulSoup(get_page.text, "html.parser")
    except requests.exceptions.RequestException as error:
        logger.critical(error)
        sys.exit(11)

    if not os.path.exists(os.path.join(output, changed_url + POSTFIX)):

        try:
            os.makedirs(os.path.join(output, changed_url + POSTFIX))
            logger.warning('Created folder {}'.format(os.path.join(output, changed_url + POSTFIX)))
        except OSError as error:
            logger.critical(error)
            sys.exit(21)

    parser(page, url, changed_url, output)
    logger.info('Downloading completed')

    try:
        with open(os.path.join(output, changed_url + EXT), 'w') as path:
            path.write(page.prettify())
            logger.info('Modified page created ')
    except OSError as error:
        logger.critical(error)
        sys.exit(22)


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


def parser(dom, url, name, output):
    for attribute in ATTRIBUTES:
        param = {attribute: re.compile(r"")}
        for tag in dom.find_all(**param):
            normalized_url = url_normalization(tag[attribute], url)
            logger.debug('{} normalized to {}'.format(tag[attribute], normalized_url))
            if tag.name == 'a':
                tag[attribute] = normalized_url
            else:
                filename, file_extension = os.path.splitext(normalized_url)

                if filename.startswith('data:'):
                    continue
                changed_filename = change_url(filename)
                logger.debug('New filename for {}{} is {}{}'.format(filename, file_extension,
                                                                    changed_filename,
                                                                    file_extension))
                try:
                    get_file = requests.get(normalized_url)
                    get_file.raise_for_status()
                    file = get_file.content
                except requests.exceptions.RequestException as error:
                    logger.critical(error)
                    sys.exit(12)

                logger.debug('{} is downloaded'.format(normalized_url))
                file_path = os.path.join(output + name + POSTFIX,
                                         changed_filename + file_extension)
                try:
                    with open(file_path, 'wb') as received_file:
                        received_file.write(file)
                        logger.debug('{} is created'.format(file_path))
                except OSError as error:
                    logger.critical(error)
                    sys.exit(23)

                tag[attribute] = name + POSTFIX + changed_filename + file_extension
                logger.debug('New {} is {}'.format(attribute, tag[attribute]))


loader('httpbin.org/status/404', '/Users/alexandrlelikov/Desktop/Python', 'debug')
