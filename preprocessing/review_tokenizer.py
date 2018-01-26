from nltk.tokenize import TweetTokenizer


class ReviewTokenizerMixin:
    def tokenize(self):
        return TweetTokenizer().tokenize(self.text)
