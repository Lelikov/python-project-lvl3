import re
import os
import requests
from urllib.parse import urlparse

REGEX = r'[^a-z0-9]'
EXT = '.html'
SCHEME = 'http://'


def loader(url, output):
    parsed_url = urlparse(url)
    name = re.sub(REGEX, '-', parsed_url.netloc + parsed_url.path)
    if not parsed_url.scheme:
        url = SCHEME + url
    with open(os.path.join(output, name + EXT), 'w') as path:
        path.write(requests.get(url).text)
    print('Downloading completed')
