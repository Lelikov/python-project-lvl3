from urllib.parse import urlparse, urlunparse
import os
from page_loader.constants import SCHEME, REGEX
from page_loader.logger import logger
import re


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


def change_url(old_url):
    parsed_url = urlparse(old_url)
    changed_url = re.sub(REGEX, '-', parsed_url.netloc + parsed_url.path)
    logger.debug('{} changed to {}'.format(old_url, changed_url))
    return changed_url
