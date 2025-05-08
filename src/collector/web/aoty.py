import requests
from bs4 import BeautifulSoup
from typing import Optional

from constants import AOTY_PUBLICATION_URL, AOTY_REQUEST_HEADERS
from src.entities.publication_review import PublicationReview


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
    
    # Extract album cover URL - look for lazy-loaded images (data-src attribute)
    cover_url = None
    img_element = review_html.find('img', class_="lazyload")
    
    if img_element:
        # Check for data-src attribute first (lazy-loaded images)
        if img_element.has_attr('data-src'):
            cover_url = img_element['data-src']
        # Fallback to regular src if data-src is not available
        elif img_element.has_attr('src') and img_element['src'] != 'https://cdn.albumoftheyear.org/images/clear.gif':
            cover_url = img_element['src']
    
    # Make sure we have the full URL
    if cover_url and not cover_url.startswith('http'):
        cover_url = f"https:{cover_url}" if cover_url.startswith('//') else f"https://www.albumoftheyear.org{cover_url}"
    
    print(f"Found cover for {artist} - {release_name}: {cover_url}")

    return PublicationReview(
        artist=artist,
        release_name=release_name,
        score=score,
        link=link,
        publication_name=publication_name,
        cover_url=cover_url
    )


if __name__ == "__main__":
    reviews = get_reviews('57-the-needle-drop')
    print(reviews)