from nltk import PorterStemmer


class ReviewStemmerMixin:
    def stem(self):
        self.tokens = map(lambda token: PorterStemmer().stem(token), self.tokens)
