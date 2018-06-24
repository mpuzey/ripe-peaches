import re
import requests
from bs4 import BeautifulSoup

from constants import ARTIST_PARTS_REGEX, METACRITIC_PUBLICATION_URL, METACRITIC_REQUEST_HEADERS, \
    METACRITIC_SCRAPE_BATCH_SIZE


def get_reviews(name):

    formatted_uri = METACRITIC_PUBLICATION_URL.format(publication_name=name,
                                                      release_count=METACRITIC_SCRAPE_BATCH_SIZE)

    response = requests.get(formatted_uri, headers=METACRITIC_REQUEST_HEADERS)
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
    review_product_href = review_html.find('div', attrs={'class': 'review_product'}).a['href']
    artist_parts = re.search(ARTIST_PARTS_REGEX, review_product_href).group(1).split('-')
    artist = ' '.join([part.capitalize() for part in artist_parts])

    return {
        'artist': artist,
        'release_name': release_name,
        'score': score,
        'publication_name': publication_name,
        'date': date,
        'link': link
    }
