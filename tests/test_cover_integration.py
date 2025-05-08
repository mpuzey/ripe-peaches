import unittest
from unittest.mock import patch, MagicMock
import json
import os

from src.collector.web.aoty import get_reviews as aoty_get_reviews
from src.collector.web.metacritic import get_reviews as metacritic_get_reviews
from src.entities.publication_review import PublicationReview


class TestCoverIntegration(unittest.TestCase):

    def setUp(self):
        # Create sample review objects with cover URLs
        self.sample_reviews = [
            PublicationReview(
                artist="Test Artist 1",
                release_name="Test Album 1",
                score=90,
                publication_name="Test Publication",
                link="/test-link-1",
                date="2023-01-01",
                cover_url="https://example.com/covers/album1.jpg"
            ),
            PublicationReview(
                artist="Test Artist 2",
                release_name="Test Album 2",
                score=85,
                publication_name="Test Publication",
                link="/test-link-2",
                date="2023-01-02",
                cover_url="https://example.com/covers/album2.jpg"
            )
        ]
        
        # Sample JSON representation
        self.sample_json = json.dumps([review.to_dict() for review in self.sample_reviews])
        
    def test_serialization_with_cover_url(self):
        """Test that PublicationReview objects properly serialize cover_url to JSON"""
        for review in self.sample_reviews:
            json_dict = review.to_dict()
            self.assertIn('cover_url', json_dict)
            self.assertEqual(json_dict['cover_url'], review.cover_url)
    
    def test_deserialization_with_cover_url(self):
        """Test that PublicationReview objects properly deserialize cover_url from JSON"""
        json_data = json.dumps([review.to_dict() for review in self.sample_reviews])
        loaded_reviews = [PublicationReview.from_dict(item) for item in json.loads(json_data)]
        
        for i, review in enumerate(loaded_reviews):
            self.assertEqual(review.cover_url, self.sample_reviews[i].cover_url)
    
    @patch('src.collector.web.aoty.requests.get')
    @patch('src.collector.web.metacritic.requests.get')
    def test_extraction_from_both_sources(self, mock_metacritic_get, mock_aoty_get):
        """Test extraction from both AOTY and Metacritic sources"""
        # Mock AOTY response
        mock_aoty_response = MagicMock()
        mock_aoty_response.text = """
        <div class="albumBlock">
            <div class="albumTitle">AOTY Album</div>
            <div class="artistTitle">AOTY Artist</div>
            <div class="rating">95</div>
            <div class="ratingText"><a href="/aoty-link">Review</a></div>
            <img class="lazyload" data-src="//cdn.albumoftheyear.org/albums/aoty.jpg">
        </div>
        """
        mock_aoty_get.return_value = mock_aoty_response
        
        # Mock Metacritic response
        mock_metacritic_response = MagicMock()
        mock_metacritic_response.status_code = 200
        mock_metacritic_response.text = """
        <li class="review critic_review first_review">
            <div class="review_product"><a href="/music/metacritic-artist/metacritic-album">Metacritic Album</a></div>
            <li class="review_product_score brief_critscore"><span>90</span></li>
            <li class="review_action publication_title">Metacritic Publication</li>
            <li class="review_action post_date">2023-01-01</li>
            <div class="product_image">
                <img data-src="/image/albums/metacritic.jpg">
            </div>
        </li>
        """
        mock_metacritic_get.return_value = mock_metacritic_response
        
        # Get reviews from both sources
        aoty_reviews = aoty_get_reviews('test-publication')
        metacritic_reviews = metacritic_get_reviews('test-publication')
        
        # Verify AOTY review has cover URL
        self.assertEqual(len(aoty_reviews), 1)
        self.assertEqual(aoty_reviews[0].cover_url, "https://cdn.albumoftheyear.org/albums/aoty.jpg")
        
        # Verify Metacritic review has cover URL
        self.assertEqual(len(metacritic_reviews), 1)
        self.assertEqual(metacritic_reviews[0].cover_url, "https://www.metacritic.com/image/albums/metacritic.jpg")

    def test_sample_json_file_format(self):
        """Creates a sample JSON file to demonstrate the expected format with cover URLs"""
        # Create sample data
        sample_data = [
            {
                "artist": "Sample Artist 1",
                "release_name": "Sample Album 1",
                "score": 92,
                "publication_name": "Rolling Stone",
                "link": "/sample-link-1",
                "date": "2023-05-15",
                "cover_url": "https://example.com/covers/sample1.jpg"
            },
            {
                "artist": "Sample Artist 2",
                "release_name": "Sample Album 2",
                "score": 88,
                "publication_name": "Pitchfork",
                "link": "/sample-link-2",
                "date": "2023-06-20",
                "cover_url": "https://example.com/covers/sample2.jpg"
            }
        ]
        
        # Create directory if it doesn't exist
        os.makedirs("debug_output", exist_ok=True)
        
        # Write sample data to file
        with open("debug_output/sample_reviews_with_covers.json", "w") as f:
            json.dump(sample_data, f, indent=2)
            
        self.assertTrue(os.path.exists("debug_output/sample_reviews_with_covers.json"))
        
        # Read back the file to verify
        with open("debug_output/sample_reviews_with_covers.json", "r") as f:
            loaded_data = json.load(f)
        
        self.assertEqual(len(loaded_data), 2)
        self.assertIn("cover_url", loaded_data[0])
        self.assertIn("cover_url", loaded_data[1])


if __name__ == '__main__':
    unittest.main() 