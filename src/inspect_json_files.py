#!/usr/bin/env python
"""
Script to inspect the releases.json and scores.json files to check for cover URLs.
This will help determine if the issue is with the collection process or the display process.
"""

import json
import os
import sys

def load_json_file(file_path):
    """Load a JSON file and return its contents."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File {file_path} is not valid JSON.")
        return None
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def inspect_releases(releases_data):
    """Inspect releases data for cover URLs."""
    print("\n=== Inspecting Releases ===")
    
    if not releases_data:
        print("No releases data to inspect.")
        return
    
    total_releases = len(releases_data)
    releases_with_cover = 0
    
    # Sample a few releases to see what's in them
    print(f"Total releases: {total_releases}")
    
    # Count releases with cover URLs
    for release_id, release in releases_data.items():
        if 'cover_url' in release and release['cover_url']:
            releases_with_cover += 1
    
    print(f"Releases with cover URLs: {releases_with_cover} ({releases_with_cover/total_releases*100:.2f}%)")
    
    # Show a sample of releases
    print("\nSample releases:")
    count = 0
    for release_id, release in releases_data.items():
        if count >= 5:
            break
        
        cover_url = release.get('cover_url')
        cover_status = "✓" if cover_url else "✗"
        
        print(f"\nRelease {count+1}:")
        print(f"  ID: {release_id[:8]}...")
        print(f"  Name: {release.get('name')}")
        print(f"  Cover URL: {cover_status} {cover_url or ''}")
        
        count += 1

def inspect_scores(scores_data):
    """Inspect scores data for cover URLs."""
    print("\n=== Inspecting Scores ===")
    
    if not scores_data:
        print("No scores data to inspect.")
        return
    
    total_scores = len(scores_data)
    scores_with_cover = 0
    
    # Count scores with cover URLs
    for score_id, score in scores_data.items():
        if 'cover_url' in score and score['cover_url']:
            scores_with_cover += 1
    
    print(f"Total scores: {total_scores}")
    print(f"Scores with cover URLs: {scores_with_cover} ({scores_with_cover/total_scores*100:.2f}%)")
    
    # Show a sample of scores
    print("\nSample scores:")
    count = 0
    for score_id, score in scores_data.items():
        if count >= 5:
            break
        
        cover_url = score.get('cover_url')
        cover_status = "✓" if cover_url else "✗"
        
        print(f"\nScore {count+1}:")
        print(f"  ID: {score_id[:8]}...")
        print(f"  Release: {score.get('release_name')}")
        print(f"  Artist: {score.get('artist_name')}")
        print(f"  Score: {score.get('score')}")
        print(f"  Cover URL: {cover_status} {cover_url or ''}")
        
        count += 1

def main():
    """Main function to inspect the JSON files."""
    print("Inspecting JSON files for cover URLs...")
    
    # Default file paths
    releases_path = "releases.json"
    scores_path = "scores.json"
    
    # Allow overriding the file paths via command line arguments
    if len(sys.argv) > 1:
        releases_path = sys.argv[1]
    if len(sys.argv) > 2:
        scores_path = sys.argv[2]
    
    print(f"Releases file: {releases_path}")
    print(f"Scores file: {scores_path}")
    
    # Load the JSON files
    releases_data = load_json_file(releases_path)
    scores_data = load_json_file(scores_path)
    
    # Inspect the data
    if releases_data:
        inspect_releases(releases_data)
    
    if scores_data:
        inspect_scores(scores_data)
    
    print("\nDone!")

if __name__ == "__main__":
    main() 