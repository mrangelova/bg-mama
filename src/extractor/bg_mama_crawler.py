import time
import settings
import database
import helpers


def crawl():
    reviews_count = 0
    urls = database.load_urls('bg-mamma').splitlines()
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue
        page = helpers.make_request(url)
        data = parse_model(page)
        reviews_count += len(data)
        database.save(data, page.title.string.replace('  :: BG-Mamma', ''))
    print("\n{} comments found.".format(reviews_count))


def parse_model(page):
    reviews_list = []
    next_button = page.find(class_="uk-pagination-next")
    print('Fetching reviews for {}.'.format(page.title.string))

    try:
        while next_button:
            posts = page.find_all(class_="topic-post")

            for post in posts:
                author = post.find(class_="user-info").a.text
                date = post.find(class_="post-date").text
                text = post.find(class_="post-content-inner")
                if len(text.contents) > 1:
                    if text.contents[1].get('class', None):
                        if 'quote-wrapper' in text.contents[1]['class']:
                            text = text.text.replace(
                                str(text.contents[1].text), '')
                if not isinstance(text, str):
                    text = text.text
                reviews_list.append([date, author, text])
            if 'uk-disabled' in next_button['class']:
                next_button = None
            else:
                url = helpers.format_url(
                    next_button.next['href'], 'bg-mamma')
                soup = helpers.make_request(url)
                next_button = soup.find(class_="uk-pagination-next")
                print('.', end='', flush=True)
                time.sleep(settings.thread_sleep_seconds_between_requests)
    except Exception as e:
        print('\n')
        print("WARNING: {}".format(e))
    except KeyboardInterrupt:
        print('\n')
        print("WARNING: Fetching reviews interrupted by user.")
    return reviews_list


crawl()
