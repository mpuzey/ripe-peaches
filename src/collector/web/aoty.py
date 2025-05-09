import requests
from bs4 import BeautifulSoup
from typing import Optional, List
import concurrent.futures
import time

from constants import AOTY_PUBLICATION_URL, AOTY_REQUEST_HEADERS
from src.entities.publication_review import PublicationReview
from src.collector.utils.image_extractor import ImageExtractor, aoty_extraction_strategies
from src.collector.utils.prefetch_cache import get_cached_cover_url

# Initialize the image extractor once with a shorter delay
image_extractor = ImageExtractor(
    headers=AOTY_REQUEST_HEADERS,
    base_url="https://www.albumoftheyear.org",
    delay=0.1  # Reduced delay
)

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
    
    # Process albums in batches
    for i in range(0, len(reviews_html), BATCH_SIZE):
        batch = reviews_html[i:i+BATCH_SIZE]
        batch_reviews = process_album_batch(batch, publication_name)
        publication_reviews.extend(batch_reviews)
        # Small delay between batches to avoid overloading the server
        if i + BATCH_SIZE < len(reviews_html):
            time.sleep(1)
    
    return publication_reviews


def process_album_batch(album_batch, publication_name) -> List[PublicationReview]:
    """Process a batch of albums concurrently"""
    batch_reviews = []
    
    # Use ThreadPoolExecutor for concurrent processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all extraction tasks
        future_to_album = {
            executor.submit(extract_data, review_html, publication_name): review_html 
            for review_html in album_batch
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_album):
            review = future.result()
            if review:
                batch_reviews.append(review)
    
    return batch_reviews


def extract_data(review_html, publication_name) -> Optional[PublicationReview]:
    """Extract review data from an individual album block"""
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
    
    # Get the album URL for direct cover extraction
    album_url = None
    album_link = review_html.find('a', href=True, class_=lambda c: c and 'album' in str(c).lower())
    if album_link:
        album_url = album_link['href']
    
    # Try to get cover URL from cache first, then go to extraction
    cover_url = None
    if album_url:
        # Check the cache first
        cover_url = get_cached_cover_url(album_url, "aoty")
        
        # If not in cache, extract it
        if not cover_url:
            cover_url = image_extractor.extract_cover_url(
                album_url, 
                aoty_extraction_strategies(image_extractor.base_url)
            )
    
    # Fallback to extraction from the review HTML if needed
    if not cover_url:
        # Try multiple approaches to find the image
        img_element = review_html.find('img', class_="lazyload")
        if not img_element:
            img_element = review_html.find('img')  # Try any image
        
        if img_element:
            # Try data-src first (lazy loading)
            if img_element.has_attr('data-src'):
                cover_url = img_element['data-src']
            # Then try data-lazy-src (another lazy loading approach)
            elif img_element.has_attr('data-lazy-src'):
                cover_url = img_element['data-lazy-src']
            # Then try src
            elif img_element.has_attr('src') and img_element['src'] != 'https://cdn.albumoftheyear.org/images/clear.gif':
                cover_url = img_element['src']
    
    # Make sure we have the full URL
    if cover_url and not cover_url.startswith('http'):
        cover_url = f"https:{cover_url}" if cover_url.startswith('//') else f"https://www.albumoftheyear.org{cover_url}"

    # Only log when no cover found (reduce log volume)
    if not cover_url:
        print(f"AOTY: No cover found for {artist} - {release_name}")
        # Save the HTML for this album for debugging if no cover found
        with open(f"debug_aoty_album_{artist}_{release_name}.html", "w", encoding="utf-8") as f:
            f.write(str(review_html))

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