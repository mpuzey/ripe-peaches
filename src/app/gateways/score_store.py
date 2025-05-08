from src.app.gateways.store import Store
from config import MINIMUM_REVIEWS_COUNTED


class ScoreStore(Store):

    def __init__(self, storage_adapter, release_adapter):
        self.storage_adapter = storage_adapter
        self.release_adapter = release_adapter

    def get(self, id):
        raise NotImplemented

    def get_all(self):
        scores = self.storage_adapter.get_all()
        releases = self.release_adapter.get_all()

        for _, score in scores.items():
            release_id = score.get('release_id')
            release = releases.get(release_id)
            if not release:
                print(f'A release with ID {release_id} could not be located')
                continue
                
            # Add release data to the score
            if isinstance(release, dict):
                # Handle release as a dictionary
                if 'date' in release:
                    score['date'] = release['date']
                    
                # Add cover URL if available
                if 'cover_url' in release and release['cover_url']:
                    score['cover_url'] = release['cover_url']
            else:
                # Handle release as an object
                if hasattr(release, 'date') and release.date:
                    score['date'] = release.date
                    
                # Add cover URL if available in the release object
                if hasattr(release, 'cover_url') and release.cover_url:
                    score['cover_url'] = release.cover_url

        return {_: value for _, value in scores.items() if value.get('reviews_counted') > MINIMUM_REVIEWS_COUNTED}

    def put(self, scores):
        self.storage_adapter.put(scores)
