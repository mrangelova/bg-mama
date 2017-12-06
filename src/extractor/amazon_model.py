class AmazonModel():
    def __init__(self, title, reviews):
        super(AmazonModel, self).__init__()
        self.title = title
        self.reviews = reviews

    def __str__(self):
        return "Title: {}, Reviews: {}".format(self.title, self.reviews)
