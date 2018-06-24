from collector.collector import Collector


class ReviewScraper(Collector):

    @staticmethod
    def collect(publications, source):

        reviews = []

        for publication in publications:
            print('scraping ' + publication + ' from ' + str(source))
            publication_reviews = source.get_reviews(publication)
            reviews.extend(publication_reviews)

        print(reviews)
        return reviews
