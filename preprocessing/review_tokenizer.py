from nltk.tokenize import TweetTokenizer


class ReviewTokenizerMixin:
    def tokenize(self):
        return TweetTokenizer(preserve_case=False).tokenize(self.text)
