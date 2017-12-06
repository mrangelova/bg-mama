import database
from helpers import make_request
from amazon_model import AmazonModel
from review_model import ReviewModel


def parse_model(page):
    raw_product_name = ''
    bs_product_name = page.find('span', attrs={'id': 'productTitle'})
    if bs_product_name:
        raw_product_name = bs_product_name.text
    product_name = ''.join(raw_product_name).strip()
    print('Getting reviews for {}.'.format(product_name))

    reviews_list = []
    all_reviews_url = page.find(
       'a', attrs={'data-hook': 'see-all-reviews-link-foot'})['href']

    reviews_page = make_request(all_reviews_url)
    next_reviews_page_button = reviews_page.find(
        'li', attrs={'class': 'a-last'})
    while next_reviews_page_button:
        # TODO: Thread.sleep() ??????????????????????????????????????????
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
                review_header, review_text, review_rating)
            reviews_list.append(review_model)
        next_reviews_page_button = reviews_page.find(
            'li', attrs={'class': 'a-last'})
        if 'a-disabled' not in next_reviews_page_button['class']:
            next_url = next_reviews_page_button.find('a')['href']
            reviews_page = make_request(next_url)
        else:
            next_reviews_page_button = None

    model = AmazonModel(product_name, reviews_list)
    return model


def start_crawl():
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
    print("{} reviews found.".format(len(data.reviews)))


if __name__ == "__main__":
    start_crawl()
