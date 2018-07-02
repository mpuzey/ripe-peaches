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
    """ This function """

    reviews = []
    soup = BeautifulSoup(html, 'html.parser')
    reviews_html = soup.findAll('li', attrs={'class': 'review critic_review first_review'})
    reviews_html.extend(soup.findAll('li', attrs={'class': 'review critic_review'}))

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

    date, link = extract_full_review(review_html)

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


def extract_full_review(review_html):
    full_review = review_html.findAll('li', attrs={'class': 'review_action full_review'})

    if not full_review:
        date = review_html.find('div', attrs={'class': 'review_action post_date'}).text
        return date, None

    link = full_review[0].a['href']
    date = review_html.find('li', attrs={'class': 'review_action post_date'}).text

    return date, link
