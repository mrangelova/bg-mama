class AmazonModel():
    def __init__(self, title, title_translated, reviews):
        super(AmazonModel, self).__init__()
        self.title = title
        self.title_translated = title_translated
        self.reviews = reviews

    def __str__(self):
        return "Title: {}, Title translated: {}, Reviews: {}".format(
            self.title, self.title_translated, self.reviews)
