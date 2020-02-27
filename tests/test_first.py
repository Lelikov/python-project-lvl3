from page_loader.engine import loader
import tempfile
import os


def test_name():
    with tempfile.TemporaryDirectory() as temp_dir:
        loader('www.lelikova.ru/book', temp_dir)
        assert os.path.exists('{}/www-lelikova-ru-book.html'.format(temp_dir)) == True