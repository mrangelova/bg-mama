import numpy as np
from preprocessing.review_cleanuper import ReviewCleanuperMixin
from preprocessing.review_stemmer import ReviewStemmerMixin
from preprocessing.review_tokenizer import ReviewTokenizerMixin
from preprocessing.review_translator import ReviewTranslatorMixin


class Review(ReviewCleanuperMixin,
             ReviewTokenizerMixin,
             ReviewStemmerMixin,
             ReviewTranslatorMixin):
    def __init__(self, text, rating=np.nan, stem=False,
                 translate_text=False, src_lang='bg', dest_lang='en'):
        self.text = text
        self.rating = rating
        self.cleanup()
        if translate_text:
            self.translate(dest_lang, src_lang)
        self.tokens = self.tokenize()
        if stem:
            self.stem()

    def __str__(self):
        return "Text: {}, Rating: {}".format(self.text, self.rating)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1
