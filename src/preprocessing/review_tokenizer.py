from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords


class ReviewTokenizerMixin:
    def tokenize(self):
        # words = TweetTokenizer(preserve_case=False).tokenize(self.text)
        # newWords = []
        # stopWords = set(stopwords.words('english'))
        # for word in words:
        #     if word not in stopWords:
        #         newWords.append(word)
        # return newWords
        return TweetTokenizer(preserve_case=False).tokenize(self.text)
