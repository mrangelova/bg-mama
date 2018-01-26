import pandas as pd
import numpy as np


comments_2 = pd.read_csv('posts.csv')
comments_2['Rating'] = [np.nan] * comments_2.shape[0]
scores = {}

for row in range(comments_2.shape[0]):
    print(comments_2['Rating'][row])

print(scores)
