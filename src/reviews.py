import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.word2vec import Word2Vec
from src.extractor.settings import db_connection_string
from src.models.review_model import Review


def post2vec(tokens, vector_space, tfidf):
    size = vector_space.layer1_size
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in tokens:
        try:
            vec += vector_space[word].reshape((1, size)) * tfidf[word]
            count += 1.
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec.tolist()[0]



class Reviews(pd.DataFrame):
    COLUMN_NAMES = ['post', 'rating']

    @classmethod
    def get(self):
        dataframes = []

        for file_ in os.listdir(self.PATH):
            dataframes.append(pd.read_csv(os.path.join(self.PATH, file_),
                                          names=AmazonReviews.COLUMN_NAMES,
                                          header=None))

        all_reviews = pd.concat(dataframes).reset_index(drop=True)
        return self(all_reviews)

    def round_ratings(self):
        def round_rating(rating):
            if rating in (1, 2):
                return 1
            if rating == 3:
                return 2
            if rating in (4, 5):
                return 3

        self['rating'] = self.apply(lambda post: round_rating(post.rating), axis=1)

    def build_vector_space(self, size=100, min_count=10):
        vector_space = Word2Vec(size=size, min_count=min_count)
        vector_space.build_vocab(self.tokens.tolist())
        vector_space.train(self.tokens)

        return vector_space

    def tokenize(self):
        def to_tokens(review):
            return Review(review.post, translate_text=self.TRANSLATE).tokens

        self['tokens'] = self.apply(lambda review: to_tokens(review), axis=1)
        return self

    def tfidf(self):
        vectorizer = TfidfVectorizer(analyzer=lambda x: x, min_df=10)
        matrix = vectorizer.fit_transform(self.tokens)
        return dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))

    def vectorize(self, vector_space, tf_idf=None):
        tf_idf = tf_idf or self.tfidf()
        self['vector'] = self.apply(lambda review: post2vec(self.tokens, vector_space, tf_idf), axis=1)
        return self


class AmazonReviews(Reviews):
    PATH = os.path.join(db_connection_string, 'amazon')
    TRANSLATE = False


class BGMammaReviews(Reviews):
    PATH = os.path.join(db_connection_string, 'bg-mamma')
    TRANSLATE = True
