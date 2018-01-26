import csv
import os
import errno
import re
import settings
import encoder


def save(data, name):
    __save__(data, name)


def load_data():
    return encoder.decode(__load__(settings.db_connection_string))


def load_urls(name):
    return __load__(settings.start_file + name + '.txt')


def __save__(data, name):
    name = re.sub('[^A-Za-z0-9]+', '', name)
    if not os.path.exists(os.path.dirname(settings.db_connection_string + name + '.txt')):
        try:
            os.makedirs(os.path.dirname(
                settings.db_connection_string + name + '.txt'))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(settings.db_connection_string + name + '.txt', "w") as f:
        wr = csv.writer(f)
        wr.writerows(data)


def __load__(path):
    data = open(path).read()
    return data
