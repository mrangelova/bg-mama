import numpy as np
from src.preprocessing.review_cleanuper import ReviewCleanuperMixin
from src.preprocessing.review_stemmer import ReviewStemmerMixin
from src.preprocessing.review_tokenizer import ReviewTokenizerMixin
from src.preprocessing.review_translator import ReviewTranslatorMixin


class Review(ReviewCleanuperMixin,
             ReviewTokenizerMixin,
             ReviewStemmerMixin,
             ReviewTranslatorMixin):
    def __init__(self, text, rating=np.nan,
                 translate_text=False, dest_lang='bg', target_lang='en'):
        self.text = text
        self.rating = rating
        self.cleanup()
        self.tokenize()
        if translate_text:
            self.translate(target_lang, dest_lang)

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
