import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from src.collector.web.metacritic import extract_data, extract_reviews, get_reviews


class TestMetacriticCoverExtraction(unittest.TestCase):

    def test_extract_data_with_data_src(self):
        """Test extracting cover URL from data-src attribute"""
        html = """
        <li class="review critic_review">
            <div class="review_product"><a href="/music/artist-name/album-name">Test Album</a></div>
            <li class="review_product_score brief_critscore"><span>90</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-01</li>
            <div class="product_image">
                <img data-src="/image/albums/12345.jpg" src="placeholder.gif">
            </div>
        </li>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup)
        
        self.assertEqual(result.cover_url, "https://www.metacritic.com/image/albums/12345.jpg")
        self.assertEqual(result.artist, "Artist Name")
        self.assertEqual(result.release_name, "Test Album")
        self.assertEqual(result.score, 90)

    def test_extract_data_with_src(self):
        """Test extracting cover URL from regular src attribute"""
        html = """
        <li class="review critic_review">
            <div class="review_product"><a href="/music/artist-name/album-name">Test Album</a></div>
            <li class="review_product_score brief_critscore"><span>85</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-02</li>
            <div class="product_image">
                <img src="/image/albums/67890.jpg">
            </div>
        </li>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup)
        
        self.assertEqual(result.cover_url, "https://www.metacritic.com/image/albums/67890.jpg")

    def test_extract_data_with_full_url(self):
        """Test extracting cover URL that's already a full URL"""
        html = """
        <li class="review critic_review">
            <div class="review_product"><a href="/music/artist-name/album-name">Test Album</a></div>
            <li class="review_product_score brief_critscore"><span>80</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-03</li>
            <div class="product_image">
                <img data-src="https://www.metacritic.com/image/albums/12345.jpg">
            </div>
        </li>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup)
        
        self.assertEqual(result.cover_url, "https://www.metacritic.com/image/albums/12345.jpg")

    def test_extract_data_with_no_cover(self):
        """Test extracting data when no cover image is present"""
        html = """
        <li class="review critic_review">
            <div class="review_product"><a href="/music/artist-name/album-name">Test Album</a></div>
            <li class="review_product_score brief_critscore"><span>75</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-04</li>
        </li>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup)
        
        self.assertIsNone(result.cover_url)

    def test_extract_data_with_no_product_image(self):
        """Test extracting data when product_image div is missing"""
        html = """
        <li class="review critic_review">
            <div class="review_product"><a href="/music/artist-name/album-name">Test Album</a></div>
            <li class="review_product_score brief_critscore"><span>70</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-05</li>
            <div class="product_image">
            </div>
        </li>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_data(soup)
        
        self.assertIsNone(result.cover_url)

    @patch('src.collector.web.metacritic.requests.get')
    def test_get_reviews_with_enhanced_headers(self, mock_get):
        """Test that get_reviews uses enhanced headers and extracts cover URLs"""
        # Mock first response with 200 status code
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.text = """
        <li class="review critic_review first_review">
            <div class="review_product"><a href="/music/artist-one/album-one">Album One</a></div>
            <li class="review_product_score brief_critscore"><span>95</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-01</li>
            <div class="product_image">
                <img data-src="/image/albums/one.jpg">
            </div>
        </li>
        <li class="review critic_review">
            <div class="review_product"><a href="/music/artist-two/album-two">Album Two</a></div>
            <li class="review_product_score brief_critscore"><span>85</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-02</li>
            <div class="product_image">
                <img data-src="/image/albums/two.jpg">
            </div>
        </li>
        """
        mock_get.return_value = mock_response_success
        
        results = get_reviews('test-publication')
        
        # Verify enhanced headers were used in the request
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn('headers', kwargs)
        headers = kwargs['headers']
        self.assertIn('User-Agent', headers)
        self.assertIn('Referer', headers)
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].cover_url, "https://www.metacritic.com/image/albums/one.jpg")
        self.assertEqual(results[1].cover_url, "https://www.metacritic.com/image/albums/two.jpg")

    @patch('src.collector.web.metacritic.requests.get')
    def test_get_reviews_fallback_to_original_headers(self, mock_get):
        """Test that get_reviews falls back to original headers if enhanced headers fail"""
        # Mock first response with 403 status code (forbidden)
        mock_response_fail = MagicMock()
        mock_response_fail.status_code = 403
        
        # Mock second response with 200 status code
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.text = """
        <li class="review critic_review first_review">
            <div class="review_product"><a href="/music/artist-one/album-one">Album One</a></div>
            <li class="review_product_score brief_critscore"><span>95</span></li>
            <li class="review_action publication_title">Test Publication</li>
            <li class="review_action post_date">2023-01-01</li>
            <div class="product_image">
                <img src="/image/albums/one.jpg">
            </div>
        </li>
        """
        mock_get.side_effect = [mock_response_fail, mock_response_success]
        
        results = get_reviews('test-publication')
        
        # Verify both sets of headers were tried
        self.assertEqual(mock_get.call_count, 2)
        
        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].cover_url, "https://www.metacritic.com/image/albums/one.jpg")


if __name__ == '__main__':
    unittest.main() 