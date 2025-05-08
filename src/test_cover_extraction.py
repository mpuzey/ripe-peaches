#!/usr/bin/env python
"""
Test script to validate that we can extract cover URLs from publication pages.
This is a standalone script that can be run to check if the HTML parsing is working correctly.
"""

import requests
from bs4 import BeautifulSoup
import json

# URLs to test
AOTY_TEST_URL = "https://www.albumoftheyear.org/publication/35-rolling-stone/"
METACRITIC_TEST_URL = "https://www.metacritic.com/publication/pitchfork"

# Request headers to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def test_aoty_cover_extraction():
    """Test extracting album covers from Album of the Year website."""
    print("\n=== Testing Album of the Year cover extraction ===")
    
    try:
        # Fetch the page
        response = requests.get(AOTY_TEST_URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch AOTY page: {response.status_code}")
            return
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find album blocks
        album_blocks = soup.findAll('div', attrs={'class': 'albumBlock'})
        print(f"Found {len(album_blocks)} album blocks")
        
        if not album_blocks:
            print("No album blocks found. The HTML structure may have changed.")
            # Save HTML for inspection
            with open("aoty_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Saved HTML to aoty_debug.html for inspection")
            return
        
        results = []
        
        # Inspect first 5 album blocks
        for i, album_block in enumerate(album_blocks[:5]):
            # Extract basic info
            release_name_elem = album_block.find('div', attrs={'class': 'albumTitle'})
            artist_elem = album_block.find('div', attrs={'class': 'artistTitle'})
            
            if not release_name_elem or not artist_elem:
                print(f"Album block {i+1} is missing title or artist")
                continue
                
            release_name = release_name_elem.text.strip()
            artist = artist_elem.text.strip()
            
            # Extract cover URL
            cover_url = None
            album_image = album_block.find('div', attrs={'class': 'albumImage'})
            
            if album_image and album_image.find('img'):
                cover_url = album_image.find('img').get('src')
                # Make sure we have the full URL
                if cover_url and not cover_url.startswith('http'):
                    cover_url = f"https:{cover_url}" if cover_url.startswith('//') else f"https://www.albumoftheyear.org{cover_url}"
            
            # Add to results
            result = {
                "artist": artist,
                "release_name": release_name,
                "cover_url": cover_url
            }
            results.append(result)
            
            # Print result
            print(f"\nAlbum {i+1}:")
            print(f"  Artist: {artist}")
            print(f"  Release: {release_name}")
            print(f"  Cover URL: {cover_url}")
            
        # Save results for reference
        with open("aoty_covers.json", "w") as f:
            json.dump(results, f, indent=2)
            
        print(f"\nSaved {len(results)} results to aoty_covers.json")
        
    except Exception as e:
        print(f"Error testing AOTY cover extraction: {e}")

def test_metacritic_cover_extraction():
    """Test extracting album covers from Metacritic website."""
    print("\n=== Testing Metacritic cover extraction ===")
    
    try:
        # Fetch the page
        response = requests.get(METACRITIC_TEST_URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch Metacritic page: {response.status_code}")
            return
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find review items
        reviews_html = soup.findAll('li', attrs={'class': 'review critic_review first_review'})
        reviews_html.extend(soup.findAll('li', attrs={'class': 'review critic_review'}))
        
        print(f"Found {len(reviews_html)} review items")
        
        if not reviews_html:
            print("No review items found. The HTML structure may have changed.")
            # Save HTML for inspection
            with open("metacritic_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Saved HTML to metacritic_debug.html for inspection")
            return
        
        results = []
        
        # Inspect first 5 reviews
        for i, review_html in enumerate(reviews_html[:5]):
            # Extract basic info
            release_elem = review_html.find('div', attrs={'class': 'review_product'})
            if not release_elem or not release_elem.a:
                print(f"Review {i+1} is missing release info")
                continue
                
            release_name = release_elem.a.text.strip()
            
            # Extract artist name from URL (simplified for this test)
            review_product_href = release_elem.a.get('href', '')
            artist = "Unknown"  # We would normally parse this more carefully
            
            # Extract cover URL
            cover_url = None
            product_image = review_html.find('div', attrs={'class': 'product_image'})
            
            if product_image and product_image.find('img'):
                cover_url = product_image.find('img').get('src')
                # Make sure we have the full URL
                if cover_url and not cover_url.startswith('http'):
                    cover_url = f"https://www.metacritic.com{cover_url}"
            
            # Add to results
            result = {
                "artist": artist,
                "release_name": release_name,
                "cover_url": cover_url
            }
            results.append(result)
            
            # Print result
            print(f"\nReview {i+1}:")
            print(f"  Artist: {artist}")
            print(f"  Release: {release_name}")
            print(f"  Cover URL: {cover_url}")
            
        # Save results for reference
        with open("metacritic_covers.json", "w") as f:
            json.dump(results, f, indent=2)
            
        print(f"\nSaved {len(results)} results to metacritic_covers.json")
        
    except Exception as e:
        print(f"Error testing Metacritic cover extraction: {e}")

if __name__ == "__main__":
    test_aoty_cover_extraction()
    test_metacritic_cover_extraction()
    print("\nDone!") 