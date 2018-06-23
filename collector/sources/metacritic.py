import requests
from bs4 import BeautifulSoup

COLLECTION_SIZE = 60
URL = 'http://www.metacritic.com/publication/{publication_name}' \
      '?filter=music&num_items={release_count}'

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def get_reviews(name):

    formatted_uri = URL.format(publication_name=name, release_count=COLLECTION_SIZE)
    response = requests.get(formatted_uri, headers=REQUEST_HEADERS)
    html = response.text
    return extract_reviews(html)


def extract_reviews(html):

    reviews = []
    reviews_html = BeautifulSoup(html, 'html.parser')\
        .findAll('li', attrs={'class': 'review critic_review'})
    for review_html in reviews_html:
        review = extract_data(review_html)
        reviews.append(review)

    return reviews


def extract_data(review_html):

    release_name = review_html.find('div', attrs={'class': 'review_product'}).a.text
    score = review_html.find('li',
                             attrs={'class': 'review_product_score brief_critscore'}).span.text
    publication_name = review_html.find('li',
                                        attrs={'class': 'review_action publication_title'}).text
    date = review_html.find('li', attrs={'class': 'review_action post_date'}).text
    link = review_html.find('li', attrs={'class': 'review_action full_review'}).a['href']

    return {
        'release_name': release_name,
        'score': score,
        'publication_name': publication_name,
        'date': date,
        'link': link
    }
