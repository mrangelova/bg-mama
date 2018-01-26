from nltk import PorterStemmer


class ReviewStemmerMixin:
    def stem(self):
        return [PorterStemmer().stem() for token in self.tokens]
