from nltk import PorterStemmer


class ReviewStemmerMixin:
    def stem(self):
        self.tokens = list(map(lambda token: PorterStemmer().stem(token), self.tokens))
