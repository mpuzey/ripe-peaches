import requests
from bs4 import BeautifulSoup
from typing import Optional, List
import concurrent.futures
import time

from constants import AOTY_PUBLICATION_URL, AOTY_REQUEST_HEADERS
from src.entities.publication_review import PublicationReview

# Maximum number of concurrent requests
MAX_WORKERS = 5
# Maximum batch size for processing albums
BATCH_SIZE = 10

def get_reviews(publication_name) -> [PublicationReview]:
    """Get reviews from Album of the Year for a specific publication"""
    formatted_uri = AOTY_PUBLICATION_URL.format(publication_name=publication_name)
    response = requests.get(formatted_uri, headers=AOTY_REQUEST_HEADERS)
    html = response.text
    reviews = extract_reviews(html, publication_name)
    return reviews

def extract_reviews(html, publication_name) -> [PublicationReview]:
    """Extract reviews from the AOTY publication page HTML"""
    publication_reviews = []
    reviews_html = BeautifulSoup(html, 'html.parser')\
        .findAll('div', attrs={'class': 'albumBlock'})
    print(f"AOTY: Found {len(reviews_html)} album blocks for {publication_name}")
    for i in range(0, len(reviews_html), BATCH_SIZE):
        batch = reviews_html[i:i+BATCH_SIZE]
        batch_reviews = process_album_batch(batch, publication_name)
        publication_reviews.extend(batch_reviews)
        if i + BATCH_SIZE < len(reviews_html):
            time.sleep(1)
    return publication_reviews

def process_album_batch(album_batch, publication_name) -> List[PublicationReview]:
    batch_reviews = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_album = {
            executor.submit(extract_data, review_html, publication_name): review_html 
            for review_html in album_batch
        }
        for future in concurrent.futures.as_completed(future_to_album):
            review = future.result()
            if review:
                batch_reviews.append(review)
    return batch_reviews

def extract_data(review_html, publication_name) -> Optional[PublicationReview]:
    release_name = review_html.find('div', attrs={'class': 'albumTitle'}).text
    rating = review_html.find('div', attrs={'class': 'rating'})
    artist = review_html.find('div', attrs={'class': 'artistTitle'}).text
    if not rating:
        return None
    link_element = review_html.find('div', attrs={'class': 'ratingText'})
    if not link_element or not link_element.find('a'):
        print(f"AOTY: No link found for {artist} - {release_name}")
        return None
    link = link_element.a['href']
    score = int(rating.text)
    # Do not attempt to extract or store cover_url for AOTY
    cover_url = None
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