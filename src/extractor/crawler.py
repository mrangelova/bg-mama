import time

import database
import settings
from translator import translate
from helpers import make_request
from amazon_model import AmazonModel
from review_model import ReviewModel


def parse_model(page):
    reviews_list = []

    # Try fetching all reviews
    # If exception return all reviews so far
    try:
        raw_product_name = ''
        bs_product_name = page.find('span', attrs={'id': 'productTitle'})
        if bs_product_name:
            raw_product_name = bs_product_name.text
        product_name = ''.join(raw_product_name).strip()
        print('Fetching reviews for {}.'.format(product_name))

        # Getting "Show all reviews" button
        all_reviews_url = page.find(
            'a', attrs={'data-hook': 'see-all-reviews-link-foot'})['href']

        reviews_page = make_request(all_reviews_url)
        next_reviews_page_button = reviews_page.find(
            'li', attrs={'class': 'a-last'})
        while next_reviews_page_button:
            reviews = reviews_page.findAll(
                'div', attrs={'data-hook': 'review'})
            for review in reviews:
                raw_review_rating = review.find(
                    'i', attrs={'data-hook': 'review-star-rating'}).text
                review_text = review.find(
                    'span', attrs={'data-hook': 'review-body'}).text
                review_header = review.find(
                    'a', attrs={'data-hook': 'review-title'}).text

                review_rating = ''.join(raw_review_rating).replace(
                    ' out of 5 stars', '')

                review_model = ReviewModel(
                    review_header, translate(review_header), review_text,
                    translate(review_text), review_rating)
                reviews_list.append(review_model)
            next_reviews_page_button = reviews_page.find(
                'li', attrs={'class': 'a-last'})
            if 'a-disabled' not in next_reviews_page_button['class']:
                next_url = next_reviews_page_button.find('a')['href']
                reviews_page = make_request(next_url)
                print('.', end='', flush=True)
                time.sleep(settings.thread_sleep_seconds_between_requests)
            else:
                next_reviews_page_button = None
                print('.')
    except Exception as e:
        print('\n')
        print("WARNING: {}".format(e))
    except KeyboardInterrupt:
        print('\n')
        print("WARNING: Fetching reviews interrupted by user.")
    model = AmazonModel(product_name or "No name",
                        translate(product_name), reviews_list)
    return model


def start_crawl():
    urls = database.load_urls().splitlines()
    result = []
    reviews_count = 0
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue

        page = make_request(url)
        data = parse_model(page)
        result.append(data)
        reviews_count += len(data.reviews)
    database.save(result)
    print("{} reviews found.".format(reviews_count))


if __name__ == "__main__":
    start_crawl()
