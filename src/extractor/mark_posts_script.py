import os
import csv
import pandas as pd
import numpy as np

csvfile_write = open('posts_new.csv', 'w', encoding='utf-8')
writer = csv.writer(csvfile_write)
writer.writerow(["Time", "Author", "Post", "Rating"])

comments_2 = pd.read_csv('posts.csv')
comments_2['Rating'] = [np.nan] * comments_2.shape[0]

for row in range(comments_2.shape[0]):
    print(row, "/", comments_2.shape[0])
    print(comments_2.iloc[row]['Post'])
    print('\n')
    comments_2.set_value(row, 'Rating', input('Rating:'))
    writer.writerow(comments_2.iloc[row])
    os.system('cls')
