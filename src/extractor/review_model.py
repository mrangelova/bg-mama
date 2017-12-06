class ReviewModel():
    def __init__(self, header, text, rating):
        super(ReviewModel, self).__init__()
        self.header = header
        self.text = text
        self.rating = rating

    def __str__(self):
        return "Header: {}, Text: {}, Rating: {}".format(
            self.header, self.text, self.rating)
