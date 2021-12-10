from typing import Dict, List
from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review


def merge_artist_dicts(archive: Dict[str, Artist], new_artist_entries: Dict[str, Artist]) -> Dict[str, Artist]:
    archive = archive.copy()
    for artist_id, recently_reviewed_artist in new_artist_entries.items():
        if artist_id in archive:
            archive = update_artist_entry(archive, recently_reviewed_artist)
        else:
            archive[artist_id] = recently_reviewed_artist

    return archive


def update_artist_entry(archive: Dict[str, Artist], new_artist_entry: Artist) -> Dict[str, Artist]:
    artist_id = new_artist_entry.id
    archived_releases = archive.get(artist_id).releases
    recently_reviewed_releases = new_artist_entry.releases

    if not archived_releases:
        archived_releases = new_artist_entry.releases
    else:
        archived_releases = update_archived_releases(archived_releases, recently_reviewed_releases)

    archive[artist_id].releases = archived_releases

    return archive


def update_archived_releases(archived_releases: List[Release], new_release_entries: List[Release]) -> List[Release]:
    updated_releases = archived_releases.copy()
    for new_release_entry in new_release_entries:
        for archived_release in archived_releases:
            if new_release_entry.id is archived_release.id:
                updated_releases = add_review_to_release_list(updated_releases, archived_release, new_release_entry)
            else:
                updated_releases.append(new_release_entry)

    return updated_releases


def add_review_to_release_list(releases: List[Release], old_release: Release, new_release: Release) -> List[Release]:
    current_release = old_release
    combined_reviews = merge_review_lists(old_release.reviews, new_release.reviews)
    old_release.reviews = combined_reviews

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

