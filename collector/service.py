from collector.sources import metacritic, aoty
from constants import METACRITIC_CURATED_PUBLICATIONS, AOTY_CURATED_PUBLICATIONS


class CollectorService:

    def __init__(self, collector, store):
        self.collector = collector
        self.store = store

    def start(self):
        harvested_data = self.collector.collect(METACRITIC_CURATED_PUBLICATIONS, metacritic)
        harvested_data.extend(self.collector.collect(AOTY_CURATED_PUBLICATIONS, aoty))

        self.store.put(harvested_data)
