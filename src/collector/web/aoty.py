import requests
from bs4 import BeautifulSoup
from typing import Optional

from constants import AOTY_PUBLICATION_URL, AOTY_REQUEST_HEADERS
from src.collector.entities.publication_review import PublicationReview


def get_reviews(publication_name) -> [PublicationReview]:

    formatted_uri = AOTY_PUBLICATION_URL.format(publication_name=publication_name)
    response = requests.get(formatted_uri, headers=AOTY_REQUEST_HEADERS)
    html = response.text
    reviews = extract_reviews(html, publication_name)

    return reviews


def extract_reviews(html, publication_name) -> [PublicationReview]:

    publication_reviews = []
    reviews_html = BeautifulSoup(html, 'html.parser')\
        .findAll('div', attrs={'class': 'albumBlock'})
    for review_html in reviews_html:
        review = extract_data(review_html, publication_name)

        if review:
            publication_reviews.append(review)

    return publication_reviews


def extract_data(review_html, publication_name) -> Optional[PublicationReview]:

    release_name = review_html.find('div', attrs={'class': 'albumTitle'}).text
    rating = review_html.find('div', attrs={'class': 'rating'})
    artist = review_html.find('div', attrs={'class': 'artistTitle'}).text

    if not rating:
        return None

    link = review_html.find('div', attrs={'class': 'ratingText'}).a['href']
    score = int(rating.text)

    return PublicationReview(
        artist=artist,
        release_name=release_name,
        score=score,
        link=link,
        publication_name=publication_name
    )


if __name__ == "__main__":
    reviews = get_reviews('57-the-needle-drop')
    print(reviews)