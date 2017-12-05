import datetime


class amazonModel():
    def __init__(self, title, product_url, reviews, crawl_time):
        super(amazonModel, self).__init__()
        self.title = title
        self.product_url = product_url
        self.reviews = reviews
        if isinstance(crawl_time, datetime.datetime):
            self.crawl_time = crawl_time.isoformat()
        else:
            self.crawl_time = crawl_time

    def __str__(self):
        return "Title: {}, Product_URL: {}, Reviews: {}, Crawl_Time: {}".format(
            self.title, self.product_url, self.reviews, self.crawl_time)
