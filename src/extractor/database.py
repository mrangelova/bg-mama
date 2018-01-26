from os import path
from os import makedirs
import io
import csv
import errno
import re
import settings


def save(data, name):
    __save__(data, name)


def load_data():
    return __load__(settings.db_connection_string)


def load_urls(name):
    return __load__(settings.start_file + name + '.txt')


def __save__(data, name):
    name = re.sub('[^A-Za-z0-9а-юА-Ю ]+', '', name)
    file_path = path.join(
        settings.db_connection_string, name + settings.file_extention)
    if not path.exists(path.dirname(file_path)):
        try:
            makedirs(path.dirname(file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(file_path, mode="w", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerows(data)


def __load__(file_path):
    with open(file_path) as f:
        data = f.read()
    return data
