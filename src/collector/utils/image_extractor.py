"""
Utility module for extracting images from web pages
"""
import re
import time
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List, Callable
from functools import lru_cache

class ImageExtractor:
    """
    Utility class for extracting images from web pages with configurable extraction strategies
    """
    
    def __init__(self, headers: Dict, base_url: str, delay: float = 0.5, cache_size: int = 1000):
        """
        Initialize the image extractor
        
        Args:
            headers: Request headers to use for fetching pages
            base_url: Base URL to prefix relative URLs
            delay: Delay between requests to avoid rate limiting
            cache_size: Size of LRU cache for URL results
        """
        self.headers = headers
        self.base_url = base_url
        self.delay = delay
        self._url_cache = {}
        
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a web page with error handling
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content if successful, None otherwise
        """
        try:
            # Add base URL if the URL is relative
            if not url.startswith('http'):
                url = f"{self.base_url}{url}"
            
            # Check cache first
            if url in self._url_cache:
                return self._url_cache[url]
                
            # Add delay to avoid rate limiting
            time.sleep(self.delay)
            
            # Fetch the page
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to fetch page: {url} (Status: {response.status_code})")
                return None
            
            # Cache the result
            self._url_cache[url] = response.text
            return response.text
            
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            return None
    
    def extract_cover_url(self, url: str, extraction_strategies: List[Callable]) -> Optional[str]:
        """
        Extract a cover image URL from a page using multiple strategies
        
        Args:
            url: URL to fetch
            extraction_strategies: List of extraction strategies to try
            
        Returns:
            Cover URL if found, None otherwise
        """
        # Fetch the page
        html = self.fetch_page(url)
        if not html:
            return None
            
        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try primary strategies first (faster ones)
        for strategy in extraction_strategies[:2]:  # Try only the first two strategies first
            cover_url = strategy(soup, html)
            if cover_url:
                # Ensure the URL is absolute
                if not cover_url.startswith('http'):
                    cover_url = f"{self.base_url}{cover_url}" if not cover_url.startswith('//') else f"https:{cover_url}"
                return cover_url
        
        # If primary strategies fail, try secondary strategies
        for strategy in extraction_strategies[2:]:
            cover_url = strategy(soup, html)
            if cover_url:
                # Ensure the URL is absolute
                if not cover_url.startswith('http'):
                    cover_url = f"{self.base_url}{cover_url}" if not cover_url.startswith('//') else f"https:{cover_url}"
                return cover_url
                
        # If all strategies fail, try regex as a last resort
        return self.extract_image_via_regex(html)
    
    @staticmethod
    def extract_image_via_regex(html: str) -> Optional[str]:
        """
        Extract image URLs from HTML using regex
        
        Args:
            html: HTML content
            
        Returns:
            First matching image URL or None
        """
        # Look for image URLs directly in the HTML
        url_pattern = r'https?://[^"\'\s]+\.(?:jpg|jpeg|png|gif|webp)'
        matches = re.findall(url_pattern, html)
        
        # Filter for likely album cover URLs
        for url in matches:
            if any(term in url.lower() for term in ['album', 'cover', 'image', 'product']):
                return url
                
        return None

# Common extraction strategies for different sites

def metacritic_extraction_strategies(base_url: str) -> List[Callable]:
    """
    Get extraction strategies for Metacritic
    
    Args:
        base_url: Base URL for Metacritic
        
    Returns:
        List of extraction strategies
    """
    def main_image_strategy(soup, html):
        # Look for the main image
        main_image = soup.find('img', class_='product_image')
        if main_image and main_image.has_attr('src'):
            return main_image['src']
        return None
        
    def og_image_strategy(soup, html):
        # Look for og:image meta tag
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.has_attr('content'):
            return og_image['content']
        return None
        
    def large_image_strategy(soup, html):
        # Look for any image with 'large' in the class
        large_image = soup.find('img', class_=lambda c: c and 'large' in str(c).lower())
        if large_image and large_image.has_attr('src'):
            return large_image['src']
        return None
        
    def schema_image_strategy(soup, html):
        # Look for the schema.org image property
        schema_image = soup.find(lambda tag: tag.has_attr('itemprop') and tag['itemprop'] == 'image')
        if schema_image and schema_image.has_attr('src'):
            return schema_image['src']
        return None
        
    def header_image_strategy(soup, html):
        # Look for any image in the page header
        header = soup.find('div', class_='product_page_title_row')
        if header:
            header_img = header.find('img')
            if header_img and header_img.has_attr('src'):
                return header_img['src']
        return None
    
    return [
        main_image_strategy,
        og_image_strategy,
        large_image_strategy,
        schema_image_strategy,
        header_image_strategy
    ]

def aoty_extraction_strategies(base_url: str) -> List[Callable]:
    """
    Get extraction strategies for Album of the Year
    
    Args:
        base_url: Base URL for AOTY
        
    Returns:
        List of extraction strategies
    """
    def main_album_image_strategy(soup, html):
        # Look for the main album image
        main_image = soup.find('img', class_='albumImage')
        if main_image:
            if main_image.has_attr('data-src'):
                return main_image['data-src']
            elif main_image.has_attr('src'):
                return main_image['src']
        return None
    
    def og_image_strategy(soup, html):
        # Look for og:image meta tag
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.has_attr('content'):
            return og_image['content']
        return None
    
    def album_art_strategy(soup, html):
        # Look in the albumArt class
        album_art = soup.find('div', class_='albumArt')
        if album_art:
            img = album_art.find('img')
            if img:
                if img.has_attr('data-src'):
                    return img['data-src']
                elif img.has_attr('src'):
                    return img['src']
        return None
    
    def album_class_image_strategy(soup, html):
        # Look for any image with 'album' in the class
        album_image = soup.find('img', class_=lambda c: c and 'album' in str(c).lower())
        if album_image:
            if album_image.has_attr('data-src'):
                return album_image['data-src']
            elif album_image.has_attr('src'):
                return album_image['src']
        return None
    
    return [
        main_album_image_strategy,
        og_image_strategy,
        album_art_strategy,
        album_class_image_strategy
    ] 