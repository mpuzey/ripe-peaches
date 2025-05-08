#!/usr/bin/env python
"""
Debug script to analyze Album of the Year website structure and find cover image URLs.
This script attempts multiple approaches to extract the image URLs.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import os

# URLs to test
AOTY_TEST_URL = "https://www.albumoftheyear.org/publication/35-rolling-stone/"

# Request headers to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.albumoftheyear.org/'
}

def debug_aoty_extraction():
    print("=== Analyzing Album of the Year website structure ===")
    
    try:
        # Create directory for output files
        os.makedirs("debug_output", exist_ok=True)
        
        # Fetch the page
        print("Fetching page...")
        response = requests.get(AOTY_TEST_URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch AOTY page: {response.status_code}")
            return
        
        # Save the HTML for inspection
        with open("debug_output/aoty_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Saved HTML to debug_output/aoty_debug.html")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all album blocks
        album_blocks = soup.findAll('div', attrs={'class': 'albumBlock'})
        print(f"Found {len(album_blocks)} album blocks")
        
        if not album_blocks:
            print("No album blocks found. The HTML structure may have changed.")
            return
        
        # Extract and save all img tags for inspection
        print("\nExtracting all image elements in album blocks...")
        
        all_images = []
        all_image_sources = set()
        
        for i, album_block in enumerate(album_blocks[:10]):  # Analyze first 10 blocks
            album_title = album_block.find('div', attrs={'class': 'albumTitle'})
            album_name = album_title.text.strip() if album_title else f"Unknown Album {i+1}"
            
            # Approach 1: Find direct img elements
            img_tags = album_block.find_all('img')
            
            # Approach 2: Look for divs that might contain the album image
            album_image_div = album_block.find('div', attrs={'class': 'albumImage'})
            album_art_div = album_block.find('div', attrs={'class': 'album-art'})
            cover_div = album_block.find('div', attrs={'class': 'cover'})
            
            # Approach 3: Look for style attributes with background-image
            elements_with_style = album_block.find_all(lambda tag: tag.has_attr('style') and 
                                                     'background-image' in tag['style'])
            
            # Approach 4: Look for data attributes that might contain image URLs
            elements_with_data = album_block.find_all(lambda tag: any(attr.startswith('data-') 
                                                               for attr in tag.attrs))
            
            # Approach 5: Look for divs with certain class patterns
            image_div_patterns = ['cover', 'image', 'album', 'art', 'thumb']
            potential_image_divs = []
            for pattern in image_div_patterns:
                potential_image_divs.extend(album_block.find_all(lambda tag: tag.name == 'div' and 
                                                        tag.has_attr('class') and 
                                                        any(pattern in cls.lower() for cls in tag['class'])))
            
            # Save results for this album block
            album_data = {
                'album_name': album_name,
                'img_tags': [{'src': img.get('src'), 'alt': img.get('alt'), 'class': img.get('class')} 
                            for img in img_tags],
                'album_image_div': str(album_image_div) if album_image_div else None,
                'album_art_div': str(album_art_div) if album_art_div else None,
                'cover_div': str(cover_div) if cover_div else None,
                'elements_with_style': [{'tag': el.name, 'style': el['style']} 
                                      for el in elements_with_style],
                'elements_with_data': [{'tag': el.name, 'attrs': {k: v for k, v in el.attrs.items() 
                                                            if k.startswith('data-')}} 
                                     for el in elements_with_data],
                'potential_image_divs': [{'tag': el.name, 'class': el.get('class')} 
                                       for el in potential_image_divs]
            }
            
            all_images.append(album_data)
            
            # Extract and collect all image sources
            for img in img_tags:
                if img.get('src'):
                    all_image_sources.add(img.get('src'))
            
            # Extract from style attributes
            for el in elements_with_style:
                style = el.get('style', '')
                url_match = re.search(r'url\([\'"]?(.*?)[\'"]?\)', style)
                if url_match:
                    all_image_sources.add(url_match.group(1))
            
            print(f"Album {i+1}: {album_name}")
            print(f"  Images found: {len(img_tags)}")
            print(f"  Style elements found: {len(elements_with_style)}")
            print(f"  Data attributes found: {len(elements_with_data)}")
            if img_tags:
                for img in img_tags:
                    print(f"  Image src: {img.get('src')}")
            print()
        
        # Save detailed results
        with open("debug_output/aoty_image_analysis.json", "w") as f:
            json.dump(all_images, f, indent=2)
        
        # Save all unique image sources
        with open("debug_output/aoty_image_sources.txt", "w") as f:
            for src in sorted(all_image_sources):
                f.write(f"{src}\n")
        
        print(f"Saved detailed analysis to debug_output/aoty_image_analysis.json")
        print(f"Saved all image sources to debug_output/aoty_image_sources.txt")
        print(f"Found {len(all_image_sources)} unique image sources")
        
    except Exception as e:
        print(f"Error analyzing AOTY website: {e}")

if __name__ == "__main__":
    debug_aoty_extraction()
    print("\nDone!") 