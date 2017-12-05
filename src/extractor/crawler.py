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

    for review in reviews:
        raw_review_rating = review.find(
            'i', attrs={'data-hook': 'review-star-rating'}).text
        review_text = review.find(
            'div', attrs={'data-hook': 'review-collapsed'}).text
        review_header = review.find(
            'a', attrs={'data-hook': 'review-title'}).text

        review_rating = ''.join(raw_review_rating).replace(
            ' out of 5 stars', '')

        review_dict = {
            'review_header': review_header,
            'review_text': review_text,
            'review_rating': review_rating
        }
        reviews_list.append(review_dict)

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


if __name__ == "__main__":
    start_crawl()
    print("End")
