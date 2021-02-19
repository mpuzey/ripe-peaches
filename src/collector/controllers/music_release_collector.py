from src.collector.controllers.collector import Collector
from src.collector.use_cases.music_cataloger import MusicCataloger


class MusicReleaseCollector(Collector):

    def __init__(self, cataloger: MusicCataloger):
        self.external_releases = []
        self.cataloger = cataloger

    def collect(self, source, **kwargs):

        releases = source.get_releases()

        if not releases:
            print('No releases available for the following publication: %s' % repr(source))

        self.external_releases.extend(releases)

    def catalog(self):

        # TODO: using the cataloging use case at the controller is a code smell we should keep these
        #  pieces of functionality separate, the cataloger should maybe hold a collector instead
        return self.cataloger.add_releases(self.external_releases)
