from src.collector.controllers.collector import Collector
from src.collector.use_cases.music_cataloger import MusicCataloger


class MusicReviewCollector(Collector):

    def __init__(self, cataloger: MusicCataloger):
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

        # TODO: using the cataloging use case at the controller is a code smell we should keep these
        #  pieces of functionality separate, the cataloger should maybe hold a collector instead
        return self.cataloger.add_reviews(self.publication_reviews)
