import os
import errno
import settings
import encoder


def save(data):
    __save__(encoder.encode(data))


def load():
    return encoder.decode(__load__())


def __save__(data):
    if not os.path.exists(os.path.dirname(settings.db_connection_string)):
        try:
            os.makedirs(os.path.dirname(settings.db_connection_string))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(settings.db_connection_string, "w") as f:
        f.write(data)


def __load__():
    data = open(settings.db_connection_string).read()
    return data
