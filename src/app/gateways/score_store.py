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

        # Count statistics for reporting
        total_scores = len(scores)
        scores_with_covers = 0
        scores_without_covers = 0

        for score_id, score in scores.items():
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
                    print(f"Added cover URL from release dict to score {score_id}: {release['cover_url']}")
                    scores_with_covers += 1
                else:
                    scores_without_covers += 1
                    print(f"No cover URL in release dict for score {score_id}")
            else:
                # Handle release as an object
                if hasattr(release, 'date') and release.date:
                    score['date'] = release.date
                    
                # Add cover URL if available in the release object
                if hasattr(release, 'cover_url') and release.cover_url:
                    score['cover_url'] = release.cover_url
                    print(f"Added cover URL from release object to score {score_id}: {release.cover_url}")
                    scores_with_covers += 1
                else:
                    scores_without_covers += 1
                    print(f"No cover URL in release object for score {score_id}")
            
        # Print summary statistics
        print(f"Cover URL Statistics: {scores_with_covers}/{total_scores} scores have cover URLs ({scores_with_covers/total_scores*100:.1f}%)")
        
        # Filter by minimum reviews and return
        filtered_scores = {_: value for _, value in scores.items() if value.get('reviews_counted') > MINIMUM_REVIEWS_COUNTED}
        print(f"Returning {len(filtered_scores)} scores after filtering by minimum reviews")
        
        return filtered_scores

    def put(self, scores):
        # Debug: Check if any scores have cover_url before storing
        scores_with_covers = 0
        for score_id, score in scores.items():
            if 'cover_url' in score and score['cover_url']:
                scores_with_covers += 1
        
        print(f"Storing {len(scores)} scores, {scores_with_covers} have cover URLs")
        self.storage_adapter.put(scores)
