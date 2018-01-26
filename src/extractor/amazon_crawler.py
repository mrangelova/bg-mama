import time
import settings
import database
from helpers import make_request


def crawl():
    reviews_count = 0
    urls = database.load_urls('amazon').splitlines()
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue
        page = make_request(url)
        data = parse_model(page)
        reviews_count += len(data)
        title = page.title.string
        title = title.split(':')[1].strip()
        database.save(data, title)
    print("{} reviews found.".format(reviews_count))


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

                review_rating = ''.join(raw_review_rating).replace(
                    ' out of 5 stars', '')

                reviews_list.append([
                    review_text,
                    review_rating])
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
    return reviews_list


crawl()
