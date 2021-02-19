from abc import ABC, abstractmethod


class Collector(ABC):

    @abstractmethod
    def collect(self, source, **kwargs):
        pass

    @abstractmethod
    def catalog(self):
        # TODO: using the cataloging use case at the controller is a code smell we should keep these
        #  pieces of functionality separate
        pass
