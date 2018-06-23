from collector.collector import Collector
from collector.sources import metacritic


class Scraper(Collector):

    def collect(self):
        reviews = metacritic.get_publication('consequence-of-sound')
        print(reviews)
        return reviews
