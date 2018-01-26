import numpy as np
from preprocessing.review_cleanuper import ReviewCleanuperMixin
from preprocessing.review_stemmer import ReviewStemmerMixin
from preprocessing.review_tokenizer import ReviewTokenizerMixin
from preprocessing.review_translator import ReviewTranslatorMixin


class Review(ReviewCleanuperMixin,
             ReviewTokenizerMixin,
             ReviewStemmerMixin,
             ReviewTranslatorMixin,
             translate_text=False,
             target_lang='en'):
    def __init__(self, text, rating=np.nan,
                 translate_text=False, dest_lang='bg', target_lang='en'):
        self.text = text
        self.rating = rating
        self.cleanup()
        self.tokenize()
        if translate_text:
            self.translate(dest_lang, target_lang)

    def __str__(self):
        return "Text: {}, Rating: {}".format(self.text, self.rating)
