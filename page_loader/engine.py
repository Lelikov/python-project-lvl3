import os
import re
from urllib.parse import urlparse, urlunparse
import requests
from bs4 import BeautifulSoup
import logging

REGEX = r'[^A-Za-z0-9]'
EXT = '.html'
SCHEME = 'http'
POSTFIX = '_files/'
ATTRIBUTES = ['src', 'href']

logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='[%(asctime)s] %(module)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    datefmt='%d-%b-%y %H:%M:%S'
)


def loader(url, output):
    if url.endswith('/'):
        url = url[:-1]
        logging.warning('Deleted / in the end')
    changed_url = change_url(url)
    try:
        page = BeautifulSoup(requests.get(url).text, "html.parser")
    except requests.exceptions.MissingSchema:
        url = urlunparse((SCHEME, url, '', '', '', ''))
        logging.warning('URL was changed. Added http://')
        page = BeautifulSoup(requests.get(url).text, "html.parser")
    if not os.path.exists(os.path.join(output, changed_url + POSTFIX)):
        os.makedirs(os.path.join(output, changed_url + POSTFIX))
        logging.warning('Created folder {}'.format(os.path.join(output, changed_url + POSTFIX)))
    parser(page, url, changed_url, output)
    logging.info('Downloading completed')
    with open(os.path.join(output, changed_url + EXT), 'w') as path:
        path.write(page.prettify())
        logging.info('Modified page created ')


def change_url(old_url):
    parsed_url = urlparse(old_url)
    changed_url = re.sub(REGEX, '-', parsed_url.netloc + parsed_url.path)
    logging.debug('{} changed to {}'.format(old_url, changed_url))
    return changed_url


def url_normalization(path, url):
    parsed_url = urlparse(path)
    if parsed_url.scheme:
        return path
    elif parsed_url.netloc:
        logging.debug('Added {}: to {}'.format(SCHEME, path))
        return urlunparse((SCHEME, parsed_url.netloc, parsed_url.path, '', '', ''))
    elif parsed_url.path.startswith('/'):
        logging.debug('Added {} to {}'.format(url, path))
        return urlunparse((SCHEME, urlparse(url).netloc, parsed_url.path, '', '', ''))
    logging.debug('Added {}/ to {}'.format(url, path))
    return urlunparse((SCHEME, urlparse(url).netloc, urlparse(url).path + '/' + path, '', '', ''))


def parser(dom, url, name, output):
    for attribute in ATTRIBUTES:
        param = {attribute: re.compile(r"")}
        for tag in dom.find_all(**param):
            normalized_url = url_normalization(tag[attribute], url)
            logging.debug('{} normalized to {}'.format(tag[attribute], normalized_url))
            if tag.name == 'a':
                tag[attribute] = normalized_url
            else:
                filename, file_extension = os.path.splitext(normalized_url)
                if filename.startswith('data:'):
                    continue
                changed_filename = change_url(filename)
                logging.debug('New filename for {}{} is {}{}'.format(filename, file_extension,
                                                                     changed_filename,
                                                                     file_extension))
                file = requests.get(normalized_url).content
                logging.debug('{} is downloaded'.format(normalized_url))
                file_path = os.path.join(output + name + POSTFIX,
                                         changed_filename + file_extension)
                with open(file_path, 'wb') as received_file:
                    received_file.write(file)
                    logging.debug('{} is created'.format(file_path))
                tag[attribute] = name + POSTFIX + changed_filename + file_extension
                logging.debug('New {} is {}'.format(attribute, tag[attribute]))


# loader('hexlet.io', '/Users/alexandrlelikov/Desktop/Python/')
