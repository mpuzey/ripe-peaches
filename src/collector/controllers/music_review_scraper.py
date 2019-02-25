from src.collector.use_cases.collector import Collector


class MusicReviewScraper(Collector):

    def __init__(self, parser):
        self.raw_reviews = []
        self.parser = parser

    def collect(self, source, **kwargs):

        publications = kwargs.get('publications')
        for publication in publications:
            print('scraping ' + publication)
            publication_reviews = source.get_reviews(publication)

            if not publication_reviews:
                print('No reviews available for the following publication: %s' % repr(publication))

            self.raw_reviews.extend(publication_reviews)

        print('finished scraping!')

    def parse(self):

        return self.parser.parse(self.raw_reviews)
