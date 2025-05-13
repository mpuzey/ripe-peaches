from typing import Dict, List
from copy import deepcopy
from src.entities.artist import Artist
from src.entities.release import Release
from src.entities.review import Review


def merge_artist_dicts(archive: Dict[str, Artist], new_artist_entries: Dict[str, Artist]) -> Dict[str, Artist]:
    merged_archive = archive.copy()
    for artist_id, recently_reviewed_artist in new_artist_entries.items():
        if artist_id in merged_archive:
            merged_archive = update_artist_entry(merged_archive, recently_reviewed_artist)
        else:
            merged_archive[artist_id] = recently_reviewed_artist

    return merged_archive


def update_artist_entry(archive: Dict[str, Artist], new_artist_entry: Artist) -> Dict[str, Artist]:
    updated_archive = archive.copy()
    artist_id = new_artist_entry.id
    archived_artist = archive.get(artist_id)
    
    if not archived_artist:
        updated_archive[artist_id] = new_artist_entry
        return updated_archive
        
    if not _has_valid_releases(archived_artist):
        updated_archive[artist_id].releases = new_artist_entry.releases
    else:
        # Merge the releases, preserving enrichment data
        merged_releases = merge_releases(archived_artist.releases, new_artist_entry.releases)
        updated_archive[artist_id].releases = merged_releases
    return updated_archive


def _has_valid_releases(artist: Artist) -> bool:
    """Check if an artist has valid releases"""
    return artist.releases and any(artist.releases)


def merge_releases(archived_releases: List[Release], new_release_entries: List[Release]) -> List[Release]:
    # Create a dictionary of existing releases by ID for faster lookup
    archived_releases_by_id = {release.id: release for release in archived_releases if release}
    result_releases = []
    processed_new_releases = set()
    
    # First, process existing releases and update them with any new data
    result_releases = _process_existing_releases(
        archived_releases, new_release_entries, processed_new_releases
    )
    
    # Add any completely new releases
    result_releases = _add_new_releases(
        result_releases, new_release_entries, processed_new_releases, archived_releases_by_id
    )
    
    return result_releases


def _process_existing_releases(archived_releases, new_release_entries, processed_new_releases):
    """Process and update existing releases with new data"""
    result_releases = []
    for archived_release in archived_releases:
        if not archived_release:
            continue
        
        # Check if we have this release in the new data
        matching_new_releases = [r for r in new_release_entries if r.id == archived_release.id]
        
        if matching_new_releases:
            new_release = matching_new_releases[0]
            processed_new_releases.add(new_release.id)
            
            # Create a merged release, preserving enrichment data
            merged_release = _create_merged_release(archived_release, new_release)
            result_releases.append(merged_release)
        else:
            # This release isn't in new data - keep it as is
            result_releases.append(archived_release)
    return result_releases


def _create_merged_release(archived_release, new_release):
    """Create a merged release preserving enrichment data"""
    merged_release = deepcopy(archived_release)
    merged_release.reviews = merge_review_lists(archived_release.reviews, new_release.reviews)
    
    # Only update metadata fields if they're empty in the archived release
    merged_release = _update_release_metadata(merged_release, new_release)
    return merged_release


def _update_release_metadata(merged_release, new_release):
    """Update release metadata only if fields are empty in original"""
    if not merged_release.date and new_release.date:
        merged_release.date = new_release.date
    if not merged_release.type and new_release.type:
        merged_release.type = new_release.type
    if not merged_release.total_tracks and new_release.total_tracks:
        merged_release.total_tracks = new_release.total_tracks
    if not merged_release.spotify_url and new_release.spotify_url:
        merged_release.spotify_url = new_release.spotify_url
    return merged_release


def _add_new_releases(result_releases, new_release_entries, processed_new_releases, archived_releases_by_id):
    """Add new releases that weren't previously processed"""
    for new_release in new_release_entries:
        if new_release.id not in processed_new_releases and new_release.id not in archived_releases_by_id:
            result_releases.append(deepcopy(new_release))
    return result_releases


def merge_review_lists(archived_reviews: List[Review], recent_reviews: List[Review]) -> List[Review]:
    combined_reviews = archived_reviews.copy()
    existing_review_ids = {review.id for review in archived_reviews if review}
    
    # Add only reviews that don't already exist
    for recent_review in recent_reviews:
        if recent_review and recent_review.id not in existing_review_ids:
            combined_reviews.append(recent_review)
            existing_review_ids.add(recent_review.id)
    return combined_reviews

