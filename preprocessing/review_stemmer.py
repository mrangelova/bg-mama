from nltk import PorterStemmer


class ReviewStemmerMixin:
    def stem(self):
        return [PorterStemmer().stem(token.lower()) for token in self.tokens]
