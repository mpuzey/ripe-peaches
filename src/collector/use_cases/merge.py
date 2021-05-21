from typing import Dict, List
from src.collector.entities.artist import Artist
from src.collector.entities.review import Review


def merge_artist_dicts(archived_artists: Dict[str, Artist], recently_reviewed_artists: Dict[str, Artist]) -> Dict[str, Artist]:

    archived_artists = archived_artists.copy()
    for artist_id, recently_reviewed_artist in recently_reviewed_artists.items():
        if artist_id in archived_artists:
            archived_releases = archived_artists.get(artist_id).releases
            for recently_reviewed_release in recently_reviewed_artist.releases:
                if archived_releases:
                    for archived_release in archived_releases:
                        if recently_reviewed_release.id is archived_release.id:
                            combined_reviews = merge_review_lists(archived_release.reviews, recently_reviewed_release.reviews)
                            # we are saving to artists by reference here we should make this clearer
                            archived_release.reviews = combined_reviews
                        else:
                            archived_releases.append(recently_reviewed_release)
                        archived_artists[artist_id].releases = archived_releases
                else:
                    archived_artists[artist_id].releases.append(recently_reviewed_release)
        else:
            archived_artists[artist_id] = recently_reviewed_artist

    return archived_artists


def merge_review_lists(archived_reviews: List[Review], recent_reviews: List[Review]) -> List[Review]:
    combined_reviews = archived_reviews.copy()
    for recent_review in recent_reviews:
        for archived_review in archived_reviews:
            if recent_review.id is archived_review.id:
                break
            combined_reviews.append(recent_review)

    return combined_reviews
