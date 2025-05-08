import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from src.collector.web.aoty import extract_data, extract_reviews, get_reviews


class TestAOTYCoverExtraction(unittest.TestCase):

    def test_extract_data_with_data_src(self):
        """Test extracting cover URL from data-src attribute (lazy-loaded image)"""
        html = """
        <div class="albumBlock">
            <div class="albumTitle">Test Album</div>
            <div class="artistTitle">Test Artist</div>
            <div class="rating">85</div>
            <div class="ratingText"><a href="/test-link">Review</a></div>
            <img class="lazyload" data-src="//cdn.albumoftheyear.org/albums/12345.jpg" 
                 src="https://cdn.albumoftheyear.org/images/clear.gif">
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup, "test-publication")
        
        self.assertEqual(result.cover_url, "https://cdn.albumoftheyear.org/albums/12345.jpg")
        self.assertEqual(result.artist, "Test Artist")
        self.assertEqual(result.release_name, "Test Album")
        self.assertEqual(result.score, 85)

    def test_extract_data_with_src(self):
        """Test extracting cover URL from regular src attribute (no lazy loading)"""
        html = """
        <div class="albumBlock">
            <div class="albumTitle">Test Album</div>
            <div class="artistTitle">Test Artist</div>
            <div class="rating">90</div>
            <div class="ratingText"><a href="/test-link">Review</a></div>
            <img class="lazyload" src="//cdn.albumoftheyear.org/albums/67890.jpg">
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup, "test-publication")
        
        self.assertEqual(result.cover_url, "https://cdn.albumoftheyear.org/albums/67890.jpg")

    def test_extract_data_with_full_url(self):
        """Test extracting cover URL that's already a full URL"""
        html = """
        <div class="albumBlock">
            <div class="albumTitle">Test Album</div>
            <div class="artistTitle">Test Artist</div>
            <div class="rating">80</div>
            <div class="ratingText"><a href="/test-link">Review</a></div>
            <img class="lazyload" data-src="https://cdn.albumoftheyear.org/albums/12345.jpg">
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup, "test-publication")
        
        self.assertEqual(result.cover_url, "https://cdn.albumoftheyear.org/albums/12345.jpg")

    def test_extract_data_with_relative_url(self):
        """Test extracting cover URL that's a relative path"""
        html = """
        <div class="albumBlock">
            <div class="albumTitle">Test Album</div>
            <div class="artistTitle">Test Artist</div>
            <div class="rating">75</div>
            <div class="ratingText"><a href="/test-link">Review</a></div>
            <img class="lazyload" data-src="/albums/54321.jpg">
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup, "test-publication")
        
        self.assertEqual(result.cover_url, "https://www.albumoftheyear.org/albums/54321.jpg")

    def test_extract_data_with_no_cover(self):
        """Test extracting data when no cover image is present"""
        html = """
        <div class="albumBlock">
            <div class="albumTitle">Test Album</div>
            <div class="artistTitle">Test Artist</div>
            <div class="rating">70</div>
            <div class="ratingText"><a href="/test-link">Review</a></div>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup, "test-publication")
        
        self.assertIsNone(result.cover_url)

    def test_extract_data_with_clear_gif(self):
        """Test that the clear.gif placeholder is ignored"""
        html = """
        <div class="albumBlock">
            <div class="albumTitle">Test Album</div>
            <div class="artistTitle">Test Artist</div>
            <div class="rating">65</div>
            <div class="ratingText"><a href="/test-link">Review</a></div>
            <img class="lazyload" src="https://cdn.albumoftheyear.org/images/clear.gif">
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup, "test-publication")
        
        self.assertIsNone(result.cover_url)

    @patch('src.collector.web.aoty.requests.get')
    def test_get_reviews_extracts_covers(self, mock_get):
        """Test that get_reviews function properly extracts cover URLs"""
        mock_response = MagicMock()
        mock_response.text = """
        <div class="albumBlock">
            <div class="albumTitle">Album One</div>
            <div class="artistTitle">Artist One</div>
            <div class="rating">95</div>
            <div class="ratingText"><a href="/link-one">Review</a></div>
            <img class="lazyload" data-src="//cdn.albumoftheyear.org/albums/one.jpg">
        </div>
        <div class="albumBlock">
            <div class="albumTitle">Album Two</div>
            <div class="artistTitle">Artist Two</div>
            <div class="rating">85</div>
            <div class="ratingText"><a href="/link-two">Review</a></div>
            <img class="lazyload" data-src="//cdn.albumoftheyear.org/albums/two.jpg">
        </div>
        """
        mock_get.return_value = mock_response
        
        results = get_reviews('test-publication')
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].cover_url, "https://cdn.albumoftheyear.org/albums/one.jpg")
        self.assertEqual(results[1].cover_url, "https://cdn.albumoftheyear.org/albums/two.jpg")


if __name__ == '__main__':
    unittest.main() 