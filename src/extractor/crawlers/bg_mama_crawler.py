import time
import re
import helpers
import settings
from crawlers.crawler import Crawler
from model import 


class BgMammaCrawler(Crawler):
    def __parse_model__(self, page):
        reviews_list = []
        next_button = page.find(class_="uk-pagination-next")

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
                    text = text.replace('\n', '').replace(u'\xa0', u'').strip()
                    text = re.sub(r'https{0,1}:\/\/\S*', ' some_url ', text)
                if 'uk-disabled' in next_button['class']:
                    next_button = None
                    reviews_list.append(Review())
                else:
                    url = helpers.format_url(next_button.next['href'], 'bg-mamma')
                    soup = helpers.make_request(url)
                    next_button = soup.find(class_="uk-pagination-next")
                    time.sleep(settings.thread_sleep_seconds_between_requests)
        except Exception as e:
            print('\n')
            print("WARNING: {}".format(e))
        except KeyboardInterrupt:
            print('\n')
            print("WARNING: Fetching reviews interrupted by user.")
        return reviews_list
