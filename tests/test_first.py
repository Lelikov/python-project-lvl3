from page_loader.engine import loader
from page_loader.creators import create_page
import os
import tempfile
import pytest
import requests


def test_name():
    with tempfile.TemporaryDirectory() as temp_dir:
        loader('https://ru.hexlet.io/courses', temp_dir, 'info')
        assert os.path.exists('{}/ru-hexlet-io-courses.html'.format(temp_dir)) == True
        assert os.path.exists('{}/ru-hexlet-io-courses_files/'.format(temp_dir)) == True


def test_error():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(requests.exceptions.RequestException, match='2'):
            loader('http://httpbin.org/status/404', temp_dir, 'info')
        with pytest.raises(OSError, match='4'):
            loader('http://httpbin.org/status/200', '/', 'info')
        with pytest.raises(OSError, match='6'):
            create_page('/', '')