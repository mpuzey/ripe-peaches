from collector.sources import metacritic, aoty
from constants import METACRITIC_PUBLICATIONS_SAMPLE, AOTY_PUBLICATIONS_SAMPLE


class CollectorService:

    def __init__(self, collector, store):
        self.collector = collector
        self.store = store

    def start(self):
        harvested_data = self.collector.collect(METACRITIC_PUBLICATIONS_SAMPLE, metacritic)
        harvested_data.extend(self.collector.collect(AOTY_PUBLICATIONS_SAMPLE, aoty))

        self.store.put(harvested_data)
