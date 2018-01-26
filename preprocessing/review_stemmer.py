from nltk import PorterStemmer


class ReviewStemmerMixin:
    def stem(self, tokens):
        return [PorterStemmer().stem(token) for token in tokens]
