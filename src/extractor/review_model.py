class ReviewModel():
    def __init__(
            self, header, header_translated, text, text_translated, rating):
        super(ReviewModel, self).__init__()
        self.header = header
        self.header_translated = header_translated
        self.text = text
        self.text_translated = text_translated
        self.rating = rating

    def __str__(self):
        return "Header: {}, Header translated: {}, Text: {}, Text translated: {}, Rating: {}".format(
            self.header, self.header_translated, self.text,
            self.text_translated, self.rating)
