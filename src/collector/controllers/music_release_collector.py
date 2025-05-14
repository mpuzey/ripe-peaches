from src.collector.controllers.release_collector import ReleaseCollector
from src.entities.external_release import ExternalRelease


class MusicReleaseCollector(ReleaseCollector):

    def __init__(self):
        self.external_releases = []

    def collect_releases(self, source) -> [ExternalRelease]:

        external_releases = source.get_releases()

        if not external_releases:
            print(
                "No releases available for the following publication: %s" % repr(source)
            )

        self.external_releases.extend(external_releases)

        return external_releases
