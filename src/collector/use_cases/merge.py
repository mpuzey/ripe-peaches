from typing import Dict, List
from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review


def merge_artist_dicts(archived_artists: Dict[str, Artist], recently_reviewed_artists: Dict[str, Artist]) -> Dict[str, Artist]:

    archived_artists = archived_artists.copy()
    for artist_id, recently_reviewed_artist in recently_reviewed_artists.items():
        if artist_id in archived_artists:
            archived_releases = archived_artists.get(artist_id).releases
            recently_reviewed_releases = recently_reviewed_artist.releases

            if not archived_releases:
                archived_releases = recently_reviewed_artist.releases
            else:
                for recently_reviewed_release in recently_reviewed_releases:
                    for archived_release in archived_releases:
                        if recently_reviewed_release.id is archived_release.id:
                            archived_releases = add_review_to_release_list(archived_releases, archived_release, recently_reviewed_release)
                        else:
                            archived_releases.append(recently_reviewed_release)
                # archived_releases = update_archive(archived_releases, recently_reviewed_releases)

            archived_artists[artist_id].releases = archived_releases
        else:
            archived_artists[artist_id] = recently_reviewed_artist

    return archived_artists


def update_archive(archived_releases: List[Release], new_release_entries: List[Release]) -> List[Release]:
    for new_release_entry in new_release_entries:
        for archived_release in archived_releases:
            if new_release_entry.id is archived_release.id:
                archived_releases = add_review_to_release_list(archived_releases, archived_release, new_release_entry)
            else:
                archived_releases.append(new_release_entry)

            return archived_releases


def add_review_to_release_list(releases: List[Release], old_release: Release, new_release: Release) -> List[Release]:
    current_release = old_release
    combined_reviews = merge_review_lists(old_release.reviews, new_release.reviews)
    old_release.reviews = combined_reviews

    # We need to remove the existing archived release with this release.id from the archived_releases list,
    # and then append the release as we do just below
    releases.remove(old_release)
    releases.append(current_release)

    return releases


def merge_review_lists(archived_reviews: List[Review], recent_reviews: List[Review]) -> List[Review]:
    combined_reviews = archived_reviews.copy()
    for recent_review in recent_reviews:
        for archived_review in archived_reviews:
            if recent_review.id is archived_review.id:
                break
            combined_reviews.append(recent_review)

    return combined_reviews

