import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report
from amazon_reviews import AmazonReviews


def get_sparse_matrix(reviews):
    bow_transformer = CountVectorizer().fit(reviews)
    print(len(bow_transformer.vocabulary_))
    reviews = bow_transformer.transform(reviews)
    return reviews


def split_reviews_to_text_and_rating(reviews):
    rev_texts = reviews['post'].values.astype('U')
    rev_ratings = reviews['rating'].values.astype('U')
    return rev_texts, rev_ratings


def get_accuracy(nb, rev_text_test, rev_ratings_test):
    predictions = nb.predict(rev_text_test)

    print(confusion_matrix(rev_ratings_test, predictions))
    print('\n')
    print(classification_report(rev_ratings_test, predictions))


def check_if_nan(reviews):
    for review in reviews['rating']:
        if review is np.nan:
            review = 0


def multinominal_NB():
    reviews = AmazonReviews.get()
    reviews = reviews.round_ratings()
    check_if_nan(reviews)
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


multinominal_NB()
