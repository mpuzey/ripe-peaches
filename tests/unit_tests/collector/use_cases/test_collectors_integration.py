import pytest
from unittest.mock import patch, MagicMock

from src.collector.web.aoty import get_reviews as get_aoty_reviews
from src.collector.web.metacritic import get_reviews as get_metacritic_reviews
from src.entities.publication_review import PublicationReview


class TestAOTYCollector:
    """Integration tests for the AOTY collector with image extraction"""

    @patch("src.collector.web.aoty.requests.get")
    @patch("src.collector.utils.image_extractor.requests.get")
    def test_aoty_review_collection(self, mock_image_get, mock_review_get):
        """Test that AOTY reviews are collected with cover URLs"""
        # Mock the review page response
        mock_review_response = MagicMock()
        mock_review_response.status_code = 200
        mock_review_response.text = """
        <html>
        <body>
            <div class="albumBlock">
                <div class="artistTitle">Test Artist</div>
                <div class="albumTitle">Test Album</div>
                <div class="rating">85</div>
                <div class="ratingText"><a href="/album/link">Review</a></div>
                <img class="lazyload" data-src="https://cdn.albumoftheyear.org/album/test.jpg">
                <a href="/album/test-album">Album Link</a>
            </div>
        </body>
        </html>
        """
        mock_review_get.return_value = mock_review_response

        # Mock the album page response for image extraction
        mock_album_response = MagicMock()
        mock_album_response.status_code = 200
        mock_album_response.text = """
        <html>
        <head>
            <meta property="og:image" content="https://cdn.albumoftheyear.org/album/high-res.jpg">
        </head>
        <body>
            <img class="albumImage" src="https://cdn.albumoftheyear.org/album/cover.jpg">
        </body>
        </html>
        """
        mock_image_get.return_value = mock_album_response

        # Call the collector
        reviews = get_aoty_reviews("test-publication")

        # Verify the results
        assert len(reviews) == 1
        review = reviews[0]
        assert isinstance(review, PublicationReview)
        assert review.artist == "Test Artist"
        assert review.release_name == "Test Album"
        assert review.score == 85
        assert review.publication_name == "test-publication"
        
        # Verify the cover URL was extracted - we expect the direct one from the review page
        # since we're mocking and our test doesn't actually navigate to the album page
        assert review.cover_url == "https://cdn.albumoftheyear.org/album/test.jpg"


class TestMetacriticCollector:
    """Integration tests for the Metacritic collector with image extraction"""

    @patch("src.collector.web.metacritic.requests.get")
    @patch("src.collector.utils.image_extractor.requests.get")
    def test_metacritic_review_collection(self, mock_image_get, mock_review_get):
        """Test that Metacritic reviews are collected with cover URLs"""
        # Mock the review page response
        mock_review_response = MagicMock()
        mock_review_response.status_code = 200
        mock_review_response.text = """
        <html>
        <body>
            <li class="review critic_review">
                <div class="review_wrap">
                    <div class="review_content">
                        <div class="review_product"><a href="/music/test-artist/test-album">Test Album</a></div>
                        <li class="review_product_score brief_critscore"><span>80</span></li>
                        <li class="review_action publication_title">Test Publication</li>
                        <li class="review_action post_date">2023-01-01</li>
                    </div>
                </div>
            </li>
        </body>
        </html>
        """
        mock_review_get.return_value = mock_review_response

        # Mock the album page response for image extraction
        mock_album_response = MagicMock()
        mock_album_response.status_code = 200
        mock_album_response.text = """
        <html>
        <head>
            <meta property="og:image" content="https://static.metacritic.com/images/products/music/test-album.jpg">
        </head>
        </html>
        """
        mock_image_get.return_value = mock_album_response

        # Call the collector
        reviews = get_metacritic_reviews("test-publication")

        # Verify the results
        assert len(reviews) == 1
        review = reviews[0]
        assert isinstance(review, PublicationReview)
        assert review.artist == "Test Artist"
        assert review.release_name == "Test Album"
        assert review.score == 80
        assert review.publication_name == "Test Publication"
        assert review.date == "2023-01-01"
        
        # Verify the cover URL was extracted
        assert review.cover_url == "https://static.metacritic.com/images/products/music/test-album.jpg"


class TestErrorHandling:
    """Tests for error handling in the collectors"""

    @patch("src.collector.web.aoty.requests.get")
    def test_aoty_request_failure(self, mock_get):
        """Test that AOTY collector handles request failures"""
        # Mock a failed response
        mock_get.side_effect = Exception("Connection error")

        # Call the collector
        reviews = get_aoty_reviews("test-publication")

        # Verify empty results on failure
        assert reviews == []

    @patch("src.collector.web.metacritic.requests.get")
    def test_metacritic_request_failure(self, mock_get):
        """Test that Metacritic collector handles request failures"""
        # Mock a failed response (first for enhanced headers, then for regular headers)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Call the collector
        reviews = get_metacritic_reviews("test-publication")

        # Verify empty results on failure
        assert reviews == []


if __name__ == "__main__":
    pytest.main() 