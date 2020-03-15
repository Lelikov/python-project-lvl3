import os
import tempfile

import pytest
import requests

from page_loader.constants import SCHEME
from page_loader.creators import save_page
from page_loader.engine import loader
from page_loader.getters import get_file
from page_loader.normalizers import arguments_normalization, url_normalization


def test_normalizers():
    url, output = arguments_normalization('foo/bar/foo/', 'foo/bar')
    assert url == SCHEME + '://foo/bar/foo'
    assert output == 'foo/bar/'
    assert url_normalization('http://test.ru', url) == 'http://test.ru'
    assert url_normalization('//test.ru', url) == 'http://test.ru'
    assert url_normalization('/foo', url) == 'http://foo/foo'
    assert url_normalization('foo', url) == 'http://foo/bar/foo/foo'


def test_name():
    with tempfile.TemporaryDirectory() as temp_dir:
        loader('https://ru.hexlet.io/courses', temp_dir, 'info')
        assert os.path.exists('{}/ru-hexlet-io-courses.html'.format(temp_dir)) == True
        assert os.path.exists('{}/ru-hexlet-io-courses_files/'.format(temp_dir)) == True


def test_error():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(requests.exceptions.RequestException, match='2'):
            loader('http://httpbin.org/status/404', temp_dir, 'info')
        with pytest.raises(requests.exceptions.RequestException, match='3'):
            get_file('/', '', '')
        with pytest.raises(OSError, match='4'):
            loader('http://httpbin.org/status/200', '/', 'info')
        with pytest.raises(OSError, match='5'):
            get_file('http://httpbin.org/static/favicon.ico', '/', '')
        with pytest.raises(OSError, match='6'):
            save_page('/', '')
