from collector.collector import Collector


class ReviewScraper(Collector):

    def __init__(self):
        self.reviews = []

    def collect(self, publication_sources):
        """Takes a list of tuples which describes """
        for publications, source in publication_sources:

            for publication in publications:
                print('scraping ' + publication)
                publication_reviews = source.get_reviews(publication)
                self.reviews.extend(publication_reviews)

        print('finished scraping!')

    def deliver(self):
        return self.reviews
