import numpy as np


class Review(ReviewCleanuperMixin, ReviewTokenizerMixin, ReviewStemmerMixin, ReviewTranslatorMixin):
    def __init__(self, text, rating=np.nan):
        self.text = text
        self.rating = rating

    def __str__(self):
        return "Text: {}, Rating: {}".format(self.text, self.rating)
