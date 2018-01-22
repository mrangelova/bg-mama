from urllib import parse

import requests
import settings
from bs4 import BeautifulSoup


def make_request(url):
    url = format_url(url)
    try:
        r = requests.get(url, headers=settings.headers)
    except Exception as e:
        print("""WARNING: {}
Request for {} failed, trying again.""".format(e, url))
        return make_request(url)

    if r.status_code != 200:
        print("WARNING: Got a {} status code for URL: {}"
              .format(r.status_code, url))
        return make_request(url)

    return BeautifulSoup(r.content, "html.parser")


def format_url(url, site='amazon'):
    u = parse.urlparse(url)

    scheme = u.scheme or "https"
    host = u.netloc or "www." + site + ".com"
    path = u.path

    if not u.query:
        query = ""
    else:
        query = "?"
        for piece in u.query.split("&"):
            k, v = piece.split("=")
            if k in settings.allowed_params:
                query += "{}={}&".format(k, v)
        query = query[:-1]

    return "{}://{}{}{}".format(scheme, host, path, query)
