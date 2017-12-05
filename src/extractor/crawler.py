from helpers import make_request
import database


if __name__ == "__main__":
    urls = database.load_urls().splitlines()
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue

        page = make_request(url)
        database.save(str(page))
    print("End")
