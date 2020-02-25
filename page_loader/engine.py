import re
import os
import requests
from urllib.parse import urlparse

REGEX = r'[^a-z0-9]'
ext = '.html'


def loader(url, output):
    parsed_url = urlparse(url)
    name = re.sub(REGEX, '-', parsed_url.netloc + parsed_url.path)
    with open(os.path.join(output, name + ext), 'w') as path:
        path.write(requests.get(url).text)
    print('Downloading completed')
