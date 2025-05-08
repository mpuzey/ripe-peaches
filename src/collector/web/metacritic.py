import re
import requests
from bs4 import BeautifulSoup
from src.entities.publication_review import PublicationReview

from constants import ARTIST_PARTS_REGEX, METACRITIC_PUBLICATION_URL, METACRITIC_REQUEST_HEADERS
from config import METACRITIC_SCRAPE_BATCH_SIZE


def get_reviews(publication_name) -> [PublicationReview]:

    formatted_uri = METACRITIC_PUBLICATION_URL.format(publication_name=publication_name,
                                                      release_count=METACRITIC_SCRAPE_BATCH_SIZE)

    response = requests.get(formatted_uri, headers=METACRITIC_REQUEST_HEADERS)
    html = response.text
    return extract_reviews(html)


def extract_reviews(html) -> [PublicationReview]:
    """ This function """

    reviews = []
    soup = BeautifulSoup(html, 'html.parser')
    reviews_html = soup.findAll('li', attrs={'class': 'review critic_review first_review'})
    reviews_html.extend(soup.findAll('li', attrs={'class': 'review critic_review'}))

    if not reviews_html:
        return None

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
        cover_url = product_image.find('img').get('src')
        # Make sure we have the full URL
        if cover_url and not cover_url.startswith('http'):
            cover_url = f"https://www.metacritic.com{cover_url}"
    
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
        date = review_html.find('div', attrs={'class': 'review_action post_date'}).text
        return date, None

    link = full_review[0].a['href']
    date = review_html.find('li', attrs={'class': 'review_action post_date'}).text

    return date, link
