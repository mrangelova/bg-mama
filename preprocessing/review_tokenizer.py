from nltk.tokenize import TweetTokenizer


class ReviewTokenizerMixin:
    def tokenize(self):
        self.tokens = TweetTokenizer(preserve_case=False).tokenize(self.text)
