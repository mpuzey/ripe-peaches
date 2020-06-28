import requests
from bs4 import BeautifulSoup

from constants import AOTY_PUBLICATION_URL, AOTY_REQUEST_HEADERS
from src.collector.entities.publication_review import PublicationReview


def get_reviews(publication_name) -> [PublicationReview]:

    formatted_uri = AOTY_PUBLICATION_URL.format(publication_name=publication_name)
    response = requests.get(formatted_uri, headers=AOTY_REQUEST_HEADERS)
    html = response.text
    reviews = extract_reviews(html)

    for review in reviews:
        review['publication_name'] = publication_name
    return reviews


def extract_reviews(html) -> [PublicationReview]:

    publication_reviews = [PublicationReview]
    reviews_html = BeautifulSoup(html, 'html.parser')\
        .findAll('div', attrs={'class': 'albumBlock'})
    for review_html in reviews_html:
        review = extract_data(review_html)
        publication_reviews.append(review)

    return publication_reviews


def extract_data(review_html) -> PublicationReview:

    release_name = review_html.find('div', attrs={'class': 'albumTitle'}).text
    score = int(review_html.find('div', attrs={'class': 'rating'}).text)
    link = review_html.find('div', attrs={'class': 'ratingText'}).a['href']
    artist = review_html.find('div', attrs={'class': 'artistTitle'}).text

    return PublicationReview(
        artist=artist,
        release_name=release_name,
        score=score,
        link=link,
        publication_name=None,
        date=None)


if __name__ == "__main__":
    reviews = get_reviews('57-the-needle-drop')
    print(reviews)
