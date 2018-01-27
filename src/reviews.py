import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.word2vec import Word2Vec
from src.extractor.settings import db_connection_string
from src.models.review_model import Review


class Reviews(pd.DataFrame):
    COLUMN_NAMES = ['post', 'rating']

    @classmethod
    def get(cls):
        dataframes = []

        for file_ in os.listdir(cls.PATH):
            dataframes.append(pd.read_csv(os.path.join(cls.PATH, file_),
                                          names=AmazonReviews.COLUMN_NAMES,
                                          header=None))

        all_reviews = pd.concat(dataframes).reset_index(drop=True)
        return cls(all_reviews)

    @classmethod
    def post2vec(cls, tokens, vector_space, tfidf):
        size = vector_space.layer1_size
        vec = np.zeros(size).reshape((1, size))
        count = 0.
        for word in tokens:
            try:
                vec += vector_space[word].reshape((1, size)) * tfidf[word]
                count += 1.
            except ValueError:
                print(tokens)
                print(word)
                print(len(vector_space[word]))
            except KeyError:
                continue
        if count != 0:
            vec /= count
        return vec.tolist()[0]

    def plot_by_rating(self, title=''):
        self.rating.value_counts().sort_index().plot(kind='bar', title=title)

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

    def tokenize(self, stem=False):
        def to_tokens(review):
            return Review(review.post, stem=stem, translate_text=self.TRANSLATE).tokens

        self['tokens'] = self.apply(lambda review: to_tokens(review), axis=1)
        return self

    def tfidf(self):
        vectorizer = TfidfVectorizer(analyzer=lambda x: x, min_df=10)
        matrix = vectorizer.fit_transform(self.tokens)
        return dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))

    def vectorize(self, vector_space, tf_idf=None):
        tf_idf = tf_idf or self.tfidf()

        def to_vector(review):
            return Reviews.post2vec(review.tokens, vector_space, tf_idf)

        self['vector'] = self.apply(lambda review: to_vector(review), axis=1)
        return self

    def predict_rating(self, model):
        self['predicted_rating'] = self.apply(lambda post: model.predict(post.vector)[0], axis=1)
        return self


class AmazonReviews(Reviews):
    PATH = os.path.join(db_connection_string, 'amazon')
    TRANSLATE = False


class BGMammaReviews(Reviews):
    PATH = os.path.join(db_connection_string, 'bg-mamma')
    TRANSLATE = True

    def remove_irrelevant_posts(self):
        relevant_posts = BGMammaReviews(self[self.rating > 0].reset_index(drop=True))
        self.__dict__.update(relevant_posts.__dict__)
