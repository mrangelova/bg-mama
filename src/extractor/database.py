import csv
import os
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
    file_path = os.path.join(
        settings.db_connection_string, name + settings.file_extention)
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(file_path, "w") as f:
        wr = csv.writer(f)
        wr.writerows(data)


def __load__(path):
    data = open(path).read()
    return data


__save__('asd', 'asd')
