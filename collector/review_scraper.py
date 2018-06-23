from collector.collector import Collector
from collector.sources import metacritic
from constants import CURATED_METACRITIC_PUBLICATIONS

METACRITIC_PUBLICATIONS = CURATED_METACRITIC_PUBLICATIONS


class ReviewScraper(Collector):

    def collect(self):

        publications = METACRITIC_PUBLICATIONS
        reviews = []

        for publication in publications:
            print('scraping ' + publication)
            publication_reviews = metacritic.get_reviews(publication)
            reviews.extend(publication_reviews)

        print(reviews)
        return reviews
