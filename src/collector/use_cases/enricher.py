from src.collector.entities.release import Release


class Enricher:

    def __init__(self, source):
        self.source = source

    def add_release_dates(self, releases: [Release]):
        for release in releases:
            self.source.get_release_details(release)
