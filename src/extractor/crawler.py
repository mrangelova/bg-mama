import re
import json

import database
from helpers import make_request
from amazon_model import AmazonModel


def parse_model(page):
    raw_product_name = ''
    bs_product_name = page.find('span', attrs={'id': 'productTitle'})
    if bs_product_name:
        raw_product_name = bs_product_name.text
    product_name = ''.join(raw_product_name).strip()
    reviews = page.findAll('div', attrs={'data-hook': 'review'})
    reviews_list = []

    if not reviews:
        raise ValueError('unable to find reviews in page')

    # Parsing individual reviews
    for review in reviews:
        raw_review_rating = review.find(
            'i', attrs={'data-hook': 'review-star-rating'}).text
        review_text = review.find(
            'div', attrs={'data-hook': 'review-collapsed'}).text

        # raw_review_text2 = page.find(
        #     'span', attrs={'data-action': 'columnbalancing-showfullreview'})
        # raw_review_text3 = page.find(
        #     'div', attrs={'id': 'dpReviews'}).text

        # if raw_review_text2:
        #     json_loaded_review_data = json.loads(raw_review_text2[0])
        #     json_loaded_review_data_text = json_loaded_review_data['rest']
        #     cleaned_json_loaded_review_data_text = re.sub(
        #         '<.*?>', '', json_loaded_review_data_text)
        #     full_review_text = review_text + cleaned_json_loaded_review_data_text
        # else:
        #     full_review_text = review_text
        # if not raw_review_text1:
        #     full_review_text = ' '.join(' '.join(raw_review_text3).split())

        review_header = review.find(
            'a', attrs={'data-hook': 'review-title'}).text

        review_rating = ''.join(raw_review_rating).replace(
            ' out of 5 stars', '')

        raw_review_comments = review.find(
            'span', attrs={'data-hook': "review-comment"}).text
        review_comments = ''.join(raw_review_comments)
        review_comments = re.sub('[A-Za-z]', '', review_comments).strip()

        review_dict = {
            'review_comment_count': review_comments,
            'review_text': review_text,
            'review_header': review_header,
            'review_rating': review_rating,
        }
        reviews_list.append(review_dict)

    model = AmazonModel(product_name, reviews_list)
    return model


if __name__ == "__main__":
    urls = database.load_urls().splitlines()
    result = []
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue

        page = make_request(url)
        data = parse_model(page)
        result.append(data)
    database.save(result)
    print("End")
