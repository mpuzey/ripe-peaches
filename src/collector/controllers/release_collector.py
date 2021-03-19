from abc import ABC, abstractmethod
from src.collector.entities.external_release import ExternalRelease


class ReleaseCollector(ABC):

    @abstractmethod
    def collect_releases(self, source) -> [ExternalRelease]:
        pass
