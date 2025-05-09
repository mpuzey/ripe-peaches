"""
Utility for prefetching and caching album cover URLs
"""
import json
import os
import time
import concurrent.futures
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup

from src.collector.utils.image_extractor import ImageExtractor, metacritic_extraction_strategies, aoty_extraction_strategies

# Cache file paths
METACRITIC_CACHE_FILE = "metacritic_cover_cache.json"
AOTY_CACHE_FILE = "aoty_cover_cache.json"

# Maximum concurrent workers
MAX_WORKERS = 10

def load_cache(cache_file: str) -> Dict:
    """
    Load an existing cache file or create a new one
    
    Args:
        cache_file: Path to the cache file
        
    Returns:
        Dictionary of cached URLs
    """
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading cache file {cache_file}: {e}")
            return {}
    return {}

def save_cache(cache_file: str, cache: Dict) -> None:
    """
    Save cache to file
    
    Args:
        cache_file: Path to the cache file
        cache: Dictionary of cached URLs
    """
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"Error saving cache file {cache_file}: {e}")

def prefetch_metacritic_covers(urls: List[str], headers: Dict) -> Dict:
    """
    Prefetch and cache cover URLs from Metacritic album pages
    
    Args:
        urls: List of album URLs to prefetch
        headers: Request headers
        
    Returns:
        Dictionary of cached cover URLs
    """
    # Load existing cache
    cache = load_cache(METACRITIC_CACHE_FILE)
    
    # Filter URLs that are not already cached
    new_urls = [url for url in urls if url not in cache]
    if not new_urls:
        print("All Metacritic URLs already cached")
        return cache
        
    print(f"Prefetching {len(new_urls)} Metacritic album covers...")
    
    # Initialize extractor with minimal delay for batch operations
    extractor = ImageExtractor(
        headers=headers,
        base_url="https://www.metacritic.com",
        delay=0.05
    )
    
    strategies = metacritic_extraction_strategies(extractor.base_url)
    
    # Process URLs concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Create a map of futures to URLs
        future_to_url = {
            executor.submit(extractor.extract_cover_url, url, strategies): url 
            for url in new_urls
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                cover_url = future.result()
                if cover_url:
                    cache[url] = cover_url
                    # Save incrementally in case of interruption
                    if len(cache) % 10 == 0:
                        save_cache(METACRITIC_CACHE_FILE, cache)
            except Exception as e:
                print(f"Error processing {url}: {e}")
    
    # Final save
    save_cache(METACRITIC_CACHE_FILE, cache)
    print(f"Cached {len(cache)} Metacritic cover URLs")
    return cache

def prefetch_aoty_covers(urls: List[str], headers: Dict) -> Dict:
    """
    Prefetch and cache cover URLs from Album of the Year album pages
    
    Args:
        urls: List of album URLs to prefetch
        headers: Request headers
        
    Returns:
        Dictionary of cached cover URLs
    """
    # Load existing cache
    cache = load_cache(AOTY_CACHE_FILE)
    
    # Filter URLs that are not already cached
    new_urls = [url for url in urls if url not in cache]
    if not new_urls:
        print("All AOTY URLs already cached")
        return cache
        
    print(f"Prefetching {len(new_urls)} AOTY album covers...")
    
    # Initialize extractor with minimal delay for batch operations
    extractor = ImageExtractor(
        headers=headers,
        base_url="https://www.albumoftheyear.org",
        delay=0.05
    )
    
    strategies = aoty_extraction_strategies(extractor.base_url)
    
    # Process URLs concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Create a map of futures to URLs
        future_to_url = {
            executor.submit(extractor.extract_cover_url, url, strategies): url 
            for url in new_urls
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                cover_url = future.result()
                if cover_url:
                    cache[url] = cover_url
                    # Save incrementally in case of interruption
                    if len(cache) % 10 == 0:
                        save_cache(AOTY_CACHE_FILE, cache)
            except Exception as e:
                print(f"Error processing {url}: {e}")
    
    # Final save
    save_cache(AOTY_CACHE_FILE, cache)
    print(f"Cached {len(cache)} AOTY cover URLs")
    return cache

def get_cached_cover_url(url: str, source: str = "metacritic") -> Optional[str]:
    """
    Get a cached cover URL if it exists
    
    Args:
        url: Album URL to look up
        source: Source site ("metacritic" or "aoty")
        
    Returns:
        Cached cover URL or None if not found
    """
    cache_file = METACRITIC_CACHE_FILE if source.lower() == "metacritic" else AOTY_CACHE_FILE
    cache = load_cache(cache_file)
    return cache.get(url)

if __name__ == "__main__":
    # Example usage for prefetching
    from constants import METACRITIC_REQUEST_HEADERS, AOTY_REQUEST_HEADERS
    
    # Example test with a few URLs
    metacritic_urls = [
        "/music/example-album/example-artist",
        "/music/another-album/another-artist"
    ]
    
    aoty_urls = [
        "/album/example-album",
        "/album/another-album"
    ]
    
    # Prefetch covers
    metacritic_cache = prefetch_metacritic_covers(metacritic_urls, METACRITIC_REQUEST_HEADERS)
    aoty_cache = prefetch_aoty_covers(aoty_urls, AOTY_REQUEST_HEADERS)
    
    # Test retrieval
    print(get_cached_cover_url(metacritic_urls[0], "metacritic"))
    print(get_cached_cover_url(aoty_urls[0], "aoty")) 