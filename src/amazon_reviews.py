import os
import pandas as pd
from src.extractor.settings import db_connection_string


class AmazonReviews:
    COLUMN_NAMES = ['post', 'rating']
    PATH = os.path.join(db_connection_string, 'amazon')

    @classmethod
    def get(self):
        dataframes = []

        for file_ in os.listdir(AmazonReviews.PATH):
            dataframes.append(pd.read_csv(os.path.join(AmazonReviews.PATH, file_),
                                          names=AmazonReviews.COLUMN_NAMES,
                                          header=None))

        return pd.concat(dataframes).reset_index(drop=True)
