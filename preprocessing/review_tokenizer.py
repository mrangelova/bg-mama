from nltk.tokenize import TweetTokenizer


class ReviewTokenizerMixin:
    def tokenize(self):
        self.tokens = TweetTokenizer().tokenize(self.text)
