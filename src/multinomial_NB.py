from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from reviews import AmazonReviews, BGMammaReviews
import numpy as np


def get_sparse_matrix(reviews, reviews_test=[]):
    bow_transformer = CountVectorizer().fit(reviews, reviews_test)
    print(len(bow_transformer.vocabulary_))
    reviews = bow_transformer.transform(reviews)
    return reviews


def split_reviews_to_text_and_rating(reviews):
    rev_texts = reviews['post'].values.astype('U')
    rev_ratings = reviews['rating'].values.astype('U')
    return rev_texts, rev_ratings


def get_accuracy(nb, rev_text_test, rev_ratings_test):
    predictions = nb.predict(rev_text_test)
    print('Accuracy: ', accuracy_score(rev_ratings_test, predictions))
    print(classification_report(rev_ratings_test, predictions))


def multinominal_NB(reviews):
    reviews.round_ratings()
    rev_texts, rev_ratings = split_reviews_to_text_and_rating(reviews)

    rev_texts = get_sparse_matrix(rev_texts)

    # get train and test data
    rev_text_train, rev_text_test, rev_ratings_train, rev_ratings_test = train_test_split(
        rev_texts, rev_ratings, test_size=0.2)
    
    # train classifier
    nb = MultinomialNB()
    nb.fit(rev_text_train, rev_ratings_train)

    # test classifier
    get_accuracy(nb, rev_text_test, rev_ratings_test)

    
def multinominal_NB_test(reviews, test_reviews):
    reviews.round_ratings()
    test_reviews.round_ratings()
    rev_texts, rev_ratings = split_reviews_to_text_and_rating(reviews)
    rev_texts_test, rev_ratings_test = split_reviews_to_text_and_rating(test_reviews)

    rev_texts_matrix = get_sparse_matrix(rev_texts, rev_texts_test)
    rev_texts_test_matrix = get_sparse_matrix(rev_texts_test, rev_texts)
    
    # train classifier
    nb = MultinomialNB()
    nb.fit(rev_texts_matrix, rev_ratings)
    
    # test classifier
    get_accuracy(nb, rev_texts_test_matrix, rev_ratings_test)


def start():
    print('Training classifier with amazon reviews.')
    reviews_amazon = AmazonReviews.get()
    reviews_amazon = AmazonReviews(reviews_amazon.dropna())
    reviews_amazon.tokenize()
    multinominal_NB(reviews_amazon)
    
    print('Training classifier with bg-mamma reviews.')
    reviews_bgmamma = BGMammaReviews.get()
    reviews_bgmamma.remove_irrelevant_posts()
    reviews_bgmamma = BGMammaReviews(reviews_bgmamma.dropna())
    # reviews_bgmamma = reviews_bgmamma.tokenize()
    multinominal_NB(reviews_bgmamma)

    print('Training classifier with all reviews.')
    reviews_all = reviews_amazon.append(reviews_bgmamma)
    multinominal_NB(reviews_all)

    print('Classifying bg-mamma reviews with amazon train')
    multinominal_NB_test(reviews_amazon, reviews_bgmamma)

start()
