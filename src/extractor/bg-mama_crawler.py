import csv
import time
import helpers
import settings


url = "http://www.bg-mamma.com/?topic=485378"
soup = helpers.make_request(url)

next_button = soup.find(class_="uk-pagination-next")

# open file
csvfile = open('posts.csv', 'w', encoding='utf-8')
writer = csv.writer(csvfile)
# create a template
writer.writerow(["Time", "Author", "Post"])

while next_button:
    posts = soup.find_all(class_="topic-post")

    for post in posts:
        author = post.find(class_="user-info").a.text
        date = post.find(class_="post-date").text
        text = post.find(class_="post-content-inner")
        if len(text.contents) > 1:
            if text.contents[1].get('class', None):
                if 'quote-wrapper' in text.contents[1]['class']:
                    text = text.text.replace(str(text.contents[1].text), '')
        if not isinstance(text, str):
            text = text.text
        text = text.strip(' ').replace('\n', '').replace(u'\xa0', u'')
        # TODO: remove urls from string
        writer.writerow([date, author, text])
    if 'uk-disabled' in next_button['class']:
        next_button = None
    else:
        url = helpers.format_url(next_button.next['href'], 'bg-mamma')
        soup = helpers.make_request(url)
        next_button = soup.find(class_="uk-pagination-next")
        time.sleep(settings.thread_sleep_seconds_between_requests)

# close file
csvfile.close()
