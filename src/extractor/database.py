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
    if not os.path.exists(os.path.dirname(settings.db_connection_string + name + settings.file_extention)):
        try:
            os.makedirs(os.path.dirname(
                settings.db_connection_string + name + settings.file_extention))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(settings.db_connection_string + name + settings.file_extention, "w") as f:
        wr = csv.writer(f)
        wr.writerows(data)


def __load__(path):
    data = open(path).read()
    return data
