import pytest
import re
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from src.collector.utils.image_extractor import (
    ImageExtractor,
    metacritic_extraction_strategies,
    aoty_extraction_strategies
)


class TestImageExtractor:
    """Tests for the ImageExtractor class"""

    @pytest.fixture
    def extractor(self):
        """Create a test extractor"""
        headers = {"User-Agent": "Test User Agent"}
        base_url = "https://test.com"
        return ImageExtractor(headers, base_url, delay=0.0)  # No delay for tests

    @patch("src.collector.utils.image_extractor.requests.get")
    def test_fetch_page_success(self, mock_get, extractor):
        """Test successful page fetching"""
        # Mock a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test page</body></html>"
        mock_get.return_value = mock_response

        # Test absolute URL
        result = extractor.fetch_page("https://example.com/album")
        assert result == "<html><body>Test page</body></html>"
        mock_get.assert_called_with("https://example.com/album", headers=extractor.headers)

        # Test relative URL
        result = extractor.fetch_page("/album")
        assert result == "<html><body>Test page</body></html>"
        mock_get.assert_called_with("https://test.com/album", headers=extractor.headers)

    @patch("src.collector.utils.image_extractor.requests.get")
    def test_fetch_page_failure(self, mock_get, extractor):
        """Test error handling in page fetching"""
        # Mock a failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = extractor.fetch_page("https://example.com/album")
        assert result is None

        # Test exception handling
        mock_get.side_effect = Exception("Connection error")
        result = extractor.fetch_page("https://example.com/album")
        assert result is None

    def test_extract_image_via_regex(self, extractor):
        """Test regex-based image extraction"""
        # Test with image URLs
        html = """
        <html>
            <body>
                Some text with https://example.com/album_cover.jpg embedded
                and another https://example.com/not_album.png image
                and an https://example.com/album/cover.webp image
            </body>
        </html>
        """
        result = extractor.extract_image_via_regex(html)
        assert result == "https://example.com/album_cover.jpg"

        # Test with no matching URLs
        html = "<html><body>No image URLs here</body></html>"
        result = extractor.extract_image_via_regex(html)
        assert result is None

    @patch("src.collector.utils.image_extractor.ImageExtractor.fetch_page")
    def test_extract_cover_url(self, mock_fetch, extractor):
        """Test the cover URL extraction process"""
        html = "<html><body>Test page with image</body></html>"
        mock_fetch.return_value = html

        # Create a test strategy
        def test_strategy(soup, html):
            return "https://example.com/cover.jpg"

        # Test successful extraction
        result = extractor.extract_cover_url(
            "https://example.com/album",
            [test_strategy]
        )
        assert result == "https://example.com/cover.jpg"

        # Test relative URL handling in results
        def relative_strategy(soup, html):
            return "/images/cover.jpg"

        result = extractor.extract_cover_url(
            "https://example.com/album",
            [relative_strategy]
        )
        assert result == "https://test.com/images/cover.jpg"

        # Test protocol-relative URL handling
        def protocol_relative_strategy(soup, html):
            return "//example.com/images/cover.jpg"

        result = extractor.extract_cover_url(
            "https://example.com/album",
            [protocol_relative_strategy]
        )
        assert result == "https://example.com/images/cover.jpg"

        # Test failed extraction
        def failing_strategy(soup, html):
            return None

        # Mock regex method to also return None
        with patch.object(extractor, 'extract_image_via_regex', return_value=None):
            result = extractor.extract_cover_url(
                "https://example.com/album",
                [failing_strategy]
            )
            assert result is None

        # Test that it tries each strategy in order
        def first_strategy(soup, html):
            return None

        def second_strategy(soup, html):
            return "https://example.com/second.jpg"

        result = extractor.extract_cover_url(
            "https://example.com/album",
            [first_strategy, second_strategy]
        )
        assert result == "https://example.com/second.jpg"


class TestAOTYStrategies:
    """Tests for Album of the Year extraction strategies"""

    @pytest.fixture
    def strategies(self):
        """Get the AOTY strategies"""
        return aoty_extraction_strategies("https://albumoftheyear.org")

    def test_main_album_image_strategy(self, strategies):
        """Test the main album image strategy"""
        main_album_image_strategy = strategies[0]
        
        # Test with data-src attribute
        html = """
        <html><body>
            <img class="albumImage" data-src="https://albumoftheyear.org/image.jpg">
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = main_album_image_strategy(soup, html)
        assert result == "https://albumoftheyear.org/image.jpg"
        
        # Test with src attribute
        html = """
        <html><body>
            <img class="albumImage" src="https://albumoftheyear.org/image2.jpg">
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = main_album_image_strategy(soup, html)
        assert result == "https://albumoftheyear.org/image2.jpg"
        
        # Test with no album image
        html = "<html><body>No image</body></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = main_album_image_strategy(soup, html)
        assert result is None

    def test_og_image_strategy(self, strategies):
        """Test the Open Graph image strategy"""
        og_image_strategy = strategies[1]
        
        # Test with og:image present
        html = """
        <html><head>
            <meta property="og:image" content="https://albumoftheyear.org/og-image.jpg">
        </head></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = og_image_strategy(soup, html)
        assert result == "https://albumoftheyear.org/og-image.jpg"
        
        # Test with no og:image
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = og_image_strategy(soup, html)
        assert result is None

    def test_album_art_strategy(self, strategies):
        """Test the album art strategy"""
        album_art_strategy = strategies[2]
        
        # Test with image in albumArt div with data-src
        html = """
        <html><body>
            <div class="albumArt">
                <img data-src="https://albumoftheyear.org/art.jpg">
            </div>
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = album_art_strategy(soup, html)
        assert result == "https://albumoftheyear.org/art.jpg"
        
        # Test with image in albumArt div with src
        html = """
        <html><body>
            <div class="albumArt">
                <img src="https://albumoftheyear.org/art2.jpg">
            </div>
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = album_art_strategy(soup, html)
        assert result == "https://albumoftheyear.org/art2.jpg"
        
        # Test with no image in albumArt div
        html = """
        <html><body>
            <div class="albumArt"></div>
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = album_art_strategy(soup, html)
        assert result is None
        
        # Test with no albumArt div
        html = "<html><body>No album art</body></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = album_art_strategy(soup, html)
        assert result is None

    def test_album_class_image_strategy(self, strategies):
        """Test the album class image strategy"""
        album_class_image_strategy = strategies[3]
        
        # Test with image with 'album' in class and data-src
        html = """
        <html><body>
            <img class="someClass album-cover" data-src="https://albumoftheyear.org/album-class.jpg">
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = album_class_image_strategy(soup, html)
        assert result == "https://albumoftheyear.org/album-class.jpg"
        
        # Test with image with 'album' in class and src
        html = """
        <html><body>
            <img class="albumCover" src="https://albumoftheyear.org/album-class2.jpg">
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = album_class_image_strategy(soup, html)
        assert result == "https://albumoftheyear.org/album-class2.jpg"
        
        # Test with no album class image
        html = "<html><body><img class='notAlbum'></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = album_class_image_strategy(soup, html)
        assert result is None


if __name__ == "__main__":
    pytest.main() 