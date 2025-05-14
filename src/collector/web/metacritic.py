import re
import requests
from bs4 import BeautifulSoup
from src.entities.publication_review import PublicationReview
import concurrent.futures
import time
from typing import List, Optional

from constants import (
    ARTIST_PARTS_REGEX,
    METACRITIC_PUBLICATION_URL,
    METACRITIC_REQUEST_HEADERS,
)
from config import METACRITIC_SCRAPE_BATCH_SIZE

# Enhanced headers to avoid being blocked
ENHANCED_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.metacritic.com/music/constant-noise/benefits",
    "Connection": "keep-alive",
    "DNT": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
}

# Maximum number of concurrent requests
MAX_WORKERS = 5
# Maximum batch size
BATCH_SIZE = 10


def get_reviews(publication_name) -> [PublicationReview]:
    """Get reviews from Metacritic for a specific publication"""
    formatted_uri = METACRITIC_PUBLICATION_URL.format(
        publication_name=publication_name, release_count=METACRITIC_SCRAPE_BATCH_SIZE
    )

    # Try first with enhanced headers
    response = requests.get(formatted_uri, headers=ENHANCED_HEADERS)

    # If that fails, try with the original headers
    if response.status_code != 200:
        print(
            f"Request with enhanced headers failed, status: {response.status_code}. Trying with original headers..."
        )
        response = requests.get(formatted_uri, headers=METACRITIC_REQUEST_HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch Metacritic page: {response.status_code}")
        return []

    html = response.text
    return extract_reviews(html)


def extract_reviews(html) -> [PublicationReview]:
    """Extract reviews from the Metacritic HTML"""
    reviews = []
    soup = BeautifulSoup(html, "html.parser")
    reviews_html = soup.find_all(
        "li", class_=lambda c: c and "review" in c and "critic_review" in c
    )
    if not reviews_html:
        print("No review items found. The HTML structure may have changed.")
        with open("metacritic_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved HTML to metacritic_debug.html for inspection")
        return []
    print(f"Metacritic: Found {len(reviews_html)} review items")
    for i in range(0, len(reviews_html), BATCH_SIZE):
        batch = reviews_html[i : i + BATCH_SIZE]
        batch_reviews = process_review_batch(batch)
        reviews.extend(batch_reviews)
        if i + BATCH_SIZE < len(reviews_html):
            time.sleep(1)
    return reviews


def process_review_batch(review_batch) -> List[PublicationReview]:
    """Process a batch of reviews concurrently"""
    batch_reviews = []

    # Use ThreadPoolExecutor for concurrent processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all extraction tasks
        future_to_review = {
            executor.submit(extract_data, review_html): review_html
            for review_html in review_batch
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_review):
            review = future.result()
            if review:
                batch_reviews.append(review)

    return batch_reviews


def extract_data(review_html) -> Optional[PublicationReview]:
    """Extract data from an individual review HTML element"""
    release_name = review_html.find("div", attrs={"class": "review_product"}).a.text
    score = int(
        review_html.find(
            "li", attrs={"class": "review_product_score brief_critscore"}
        ).span.text
    )
    publication_name = review_html.find(
        "li", attrs={"class": "review_action publication_title"}
    ).text
    date, link = extract_full_review(review_html)
    review_product_href = review_html.find("div", attrs={"class": "review_product"}).a["href"]
    groups = re.search(ARTIST_PARTS_REGEX, review_product_href)
    print(f"DEBUG: release_name={release_name}, score={score}, publication_name={publication_name}, date={date}, link={link}, href={review_product_href}, groups={groups}")
    if not groups:
        print(
            "failed to parse metacritic html for release: %s got artist: %s"
            % (release_name, review_product_href)
        )
        return None
    artist_parts = groups.group(1).split("-")
    artist = " ".join([part.capitalize() for part in artist_parts])
    cover_url = None
    print(f"DEBUG: Returning PublicationReview(artist={artist}, release_name={release_name}, score={score}, publication_name={publication_name}, date={date}, link={link}, cover_url={cover_url})")
    return PublicationReview(
        artist=artist,
        release_name=release_name,
        score=score,
        publication_name=publication_name,
        date=date,
        link=link,
        cover_url=cover_url,
    )


def extract_full_review(review_html):
    """Extract full review link and date from a review HTML element"""
    full_review = review_html.findAll(
        "li", attrs={"class": "review_action full_review"}
    )

    if not full_review:
        # Check for date in li element first (as used in tests)
        date_element = review_html.find(
            "li", attrs={"class": "review_action post_date"}
        )
        # If not found, try div (as might be in actual website)
        if not date_element:
            date_element = review_html.find(
                "div", attrs={"class": "review_action post_date"}
            )

        if date_element:
            date = date_element.text
        else:
            # Fallback if no date element found
            date = None

        return date, None

    link = full_review[0].a["href"]

    # Check for date in li element first
    date_element = review_html.find("li", attrs={"class": "review_action post_date"})
    if not date_element:
        date_element = review_html.find(
            "div", attrs={"class": "review_action post_date"}
        )

    date = date_element.text if date_element else None

    return date, link
