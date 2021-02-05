from src.collector.controllers.collector import Collector
from src.collector.use_cases.music_catalogue import Catalogue


class MusicReviewCollector(Collector):

    def __init__(self, cataloger: Catalogue):
        self.publication_reviews = []
        self.cataloger = cataloger

    def collect(self, source, **kwargs):

        publications = kwargs.get('publications')
        for publication in publications:
            print('scraping ' + publication)
            publication_reviews = source.get_reviews(publication)

            if not publication_reviews:
                print('No reviews available for the following publication: %s' % repr(publication))

            self.publication_reviews.extend(publication_reviews)

        print('finished scraping!')

    def catalog(self):

        return self.cataloger.add_review(self.publication_reviews)
