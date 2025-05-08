import re
import requests
from bs4 import BeautifulSoup
from src.entities.publication_review import PublicationReview

from constants import ARTIST_PARTS_REGEX, METACRITIC_PUBLICATION_URL, METACRITIC_REQUEST_HEADERS
from config import METACRITIC_SCRAPE_BATCH_SIZE

# Enhanced headers to avoid being blocked
ENHANCED_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.metacritic.com/',
    'sec-ch-ua': '"Not A(Brand";v="24", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'DNT': '1',
    'Connection': 'keep-alive'
}


def get_reviews(publication_name) -> [PublicationReview]:

    formatted_uri = METACRITIC_PUBLICATION_URL.format(publication_name=publication_name,
                                                      release_count=METACRITIC_SCRAPE_BATCH_SIZE)

    # Try first with enhanced headers
    response = requests.get(formatted_uri, headers=ENHANCED_HEADERS)
    
    # If that fails, try with the original headers
    if response.status_code != 200:
        print(f"Request with enhanced headers failed, status: {response.status_code}. Trying with original headers...")
        response = requests.get(formatted_uri, headers=METACRITIC_REQUEST_HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to fetch Metacritic page: {response.status_code}")
        return []
        
    html = response.text
    return extract_reviews(html)


def extract_reviews(html) -> [PublicationReview]:
    """ This function """

    reviews = []
    soup = BeautifulSoup(html, 'html.parser')
    reviews_html = soup.findAll('li', attrs={'class': 'review critic_review first_review'})
    reviews_html.extend(soup.findAll('li', attrs={'class': 'review critic_review'}))

    if not reviews_html:
        print("No review items found. The HTML structure may have changed.")
        # Save HTML for inspection
        with open("metacritic_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved HTML to metacritic_debug.html for inspection")
        return []

    for review_html in reviews_html:
        review = extract_data(review_html)
        if review:
            reviews.append(review)

    return reviews


def extract_data(review_html) -> PublicationReview:

    release_name = review_html.find('div', attrs={'class': 'review_product'}).a.text
    score = int(review_html.find('li',
                             attrs={'class': 'review_product_score brief_critscore'}).span.text)
    publication_name = review_html.find('li',
                                        attrs={'class': 'review_action publication_title'}).text

    date, link = extract_full_review(review_html)

    review_product_href = review_html.find('div', attrs={'class': 'review_product'}).a['href']
    groups = re.search(ARTIST_PARTS_REGEX, review_product_href)

    if not groups:
        print('failed to parse metacritic html for release: %s got artist: %s' % (release_name, review_product_href))
        return None

    artist_parts = groups.group(1).split('-')
    artist = ' '.join([part.capitalize() for part in artist_parts])
    
    # Extract album cover URL - find the img element within the product_image
    cover_url = None
    product_image = review_html.find('div', attrs={'class': 'product_image'})
    if product_image and product_image.find('img'):
        # Try both data-src and src attributes
        img = product_image.find('img')
        if img.has_attr('data-src'):
            cover_url = img['data-src']
        elif img.has_attr('src'):
            cover_url = img['src']
            
        # Make sure we have the full URL
        if cover_url and not cover_url.startswith('http'):
            cover_url = f"https://www.metacritic.com{cover_url}"
    
    print(f"Found cover for {artist} - {release_name}: {cover_url}")
    
    return PublicationReview(
        artist=artist,
        release_name=release_name,
        score=score,
        publication_name=publication_name,
        date=date,
        link=link,
        cover_url=cover_url
    )


def extract_full_review(review_html):
    full_review = review_html.findAll('li', attrs={'class': 'review_action full_review'})

    if not full_review:
        # Check for date in li element first (as used in tests)
        date_element = review_html.find('li', attrs={'class': 'review_action post_date'})
        # If not found, try div (as might be in actual website)
        if not date_element:
            date_element = review_html.find('div', attrs={'class': 'review_action post_date'})
            
        if date_element:
            date = date_element.text
        else:
            # Fallback if no date element found
            date = None
            
        return date, None

    link = full_review[0].a['href']
    
    # Check for date in li element first
    date_element = review_html.find('li', attrs={'class': 'review_action post_date'})
    if not date_element:
        date_element = review_html.find('div', attrs={'class': 'review_action post_date'})
        
    date = date_element.text if date_element else None

    return date, link
