from datetime import datetime

# database
db_connection_string = "../data/db.txt"  # .format(datetime.now().strftime("%d-%m-%Y %H-%M-%S"))

# start file
start_file = "start_urls.txt"

allowed_params = ["node", "rh", "page", "pageNumber"]
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/51.0.2704.103 Safari/537.36")
}

thread_sleep_seconds_between_requests = 1
