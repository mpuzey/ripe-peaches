from collector.collector import Collector
from collector.sources import metacritic


class ReviewScraper(Collector):

    def __init__(self, publications):
        self.publications = publications

    def collect(self):

        reviews = []

        for publication in self.publications:
            print('scraping ' + publication)
            publication_reviews = metacritic.get_reviews(publication)
            reviews.extend(publication_reviews)

        print(reviews)
        return reviews
