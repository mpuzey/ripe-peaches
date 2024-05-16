from src.collector.controllers.review_collector import ReviewCollector
from src.entities.publication_review import PublicationReview


class MusicReviewCollector(ReviewCollector):

    def __init__(self):
        self.publication_reviews = []

    def collect_reviews(self, source, **kwargs) -> [PublicationReview]:

        publications = kwargs.get('publications')
        for publication in publications:
            print('scraping ' + publication)
            publication_reviews = source.get_reviews(publication)

            if not publication_reviews:
                print('No reviews available for the following publication: %s' % repr(publication))
                continue

            self.publication_reviews.extend(publication_reviews)

        print('finished scraping!')

        return self.publication_reviews
