import re
import os
import requests
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup

REGEX = r'[^A-Za-z0-9]'
EXT = '.html'
SCHEME = 'http'
PATH = '_files/'
TAGS = ['src', 'href']


def change_url(old_url):
    parsed_url = urlparse(old_url)
    return re.sub(REGEX, '-', parsed_url.netloc + parsed_url.path)


def url_normalization(path, url):
    b = urlparse(path)
    if b.scheme:
        return path
    elif b.netloc:
        return urlunparse((SCHEME, b.netloc, b.path, '', '', ''))
    elif b.path.startswith('/'):
        return urlunparse((SCHEME, urlparse(url).netloc, b.path, '', '', ''))
    return urlunparse((SCHEME, urlparse(url).netloc, urlparse(url).path + '/' + path, '', '', ''))


def parser(attr, dom, url, name, output):
    param = {attr: re.compile(r"")}
    for tag in dom.find_all(**param):
        if tag.name == 'a':
            tag[attr] = url_normalization(tag[attr], url)
        else:
            normal_url = url_normalization(tag[attr], url)
            filename, file_extension = os.path.splitext(normal_url)
            if filename.startswith('data:'):
                continue
            changed_filename = change_url(filename)
            file = requests.get(normal_url).content
            with open(os.path.join(output + name + PATH, changed_filename + file_extension),
                      'wb') as received_file:
                received_file.write(file)
            tag[attr] = name + PATH + changed_filename + file_extension


def loader(url, output):
    if url.endswith('/'):
        url = url[:-1]
    name = change_url(url)
    try:
        page = BeautifulSoup(requests.get(url).text, "html.parser")
    except requests.exceptions.MissingSchema:
        url = urlunparse((SCHEME, url, '', '', '', ''))
        print('URL was changed. Added http://')
        page = BeautifulSoup(requests.get(url).text, "html.parser")
    if not os.path.exists(os.path.join(output, name + PATH)):
        os.makedirs(os.path.join(output, name + PATH))
    for tag in TAGS:
        parser(tag, page, url, name, output)
    with open(os.path.join(output, name + EXT), 'w') as path:
        path.write(page.prettify())
    print('Downloading completed')