import asyncio
import unittest
import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock, call

from src.collector.use_cases.enricher import Enricher
from src.collector.web.spotify import RateLimitError
from src.entities.artist import Artist, Release
from src.entities.external_release import ExternalRelease
from src.entities.review import Review


class TestEnricher(unittest.TestCase):

    def setUp(self):
        self.mock_source = Mock()
        self.enricher = Enricher(self.mock_source)

    @patch('asyncio.Semaphore')
    @patch('aiohttp.ClientSession')
    def test_add_release_dates(self, mock_session, mock_semaphore):
        # Create test data
        artist = Artist('1', 'Test Artist', [Release('Test Release', 'Test Release', [], None, None, None, None)])
        artists = {'1': artist}
        
        # Setup mocks
        mock_session_instance = AsyncMock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.__aenter__.return_value = mock_session_instance
        
        mock_enrichment_source = Mock()
        self.mock_source.return_value = mock_enrichment_source
        
        # Mock the enrich_artists method to isolate the test
        with patch.object(self.enricher, 'enrich_artists', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = {'1': artist}
            
            # Run the method
            result = asyncio.run(self.enricher.add_release_dates(artists))
            
            # Assertions
            self.assertEqual(result, {'1': artist})
            self.mock_source.assert_called_once_with(mock_session_instance)
            mock_enrich.assert_called_once_with(artists, mock_enrichment_source)


@pytest.mark.asyncio
class TestEnricherAsync:
    
    def setup_method(self):
        self.mock_source = Mock()
        self.enricher = Enricher(self.mock_source)

    @patch('asyncio.sleep', new_callable=AsyncMock)
    @patch('random.uniform', return_value=1.0)  # Simplify jitter for testing
    async def test_enrich_artist_with_retries_success(self, mock_uniform, mock_sleep):
        # Setup test data
        artist = Artist('1', 'Test Artist', [Release('Test Release', 'Test Release', [], None, None, None, None)])
        mock_semaphore = AsyncMock()
        mock_enrichment_source = AsyncMock()
        
        # Setup mocks for internal methods
        with patch.object(self.enricher, 'fetch_enrichment_data', new_callable=AsyncMock) as mock_fetch:
            with patch.object(self.enricher, 'process_response', new_callable=AsyncMock) as mock_process:
                # Mock successful data fetch
                mock_fetch.return_value = {'name': 'Test Release'}
                
                # Mock successful processing
                expected_result = Artist('1', 'Test Artist', [Release('Test Release', 'Test Release', [], '2022-01-01', 'album', 10, 'https://spotify.com')])
                mock_process.return_value = expected_result
                
                # Run the method
                result = await self.enricher.enrich_artist_with_retries(mock_semaphore, mock_enrichment_source, artist)
                
                # Assertions
                assert result == expected_result
                mock_fetch.assert_called_once_with(mock_enrichment_source, artist)
                mock_process.assert_called_once_with({'name': 'Test Release'}, artist)
                mock_sleep.assert_not_called()

    @patch('asyncio.sleep', new_callable=AsyncMock)
    @patch('random.uniform', return_value=1.0)  # Simplify jitter for testing
    async def test_enrich_artist_with_rate_limit_retry(self, mock_uniform, mock_sleep):
        # Setup test data
        artist = Artist('1', 'Test Artist', [Release('Test Release', 'Test Release', [], None, None, None, None)])
        mock_semaphore = AsyncMock()
        mock_enrichment_source = AsyncMock()
        
        # Create a side effect that raises RateLimitError once, then succeeds
        fetch_results = [
            RateLimitError("Rate limit hit", retry_after=5),
            {'name': 'Test Release'}
        ]
        
        # Setup mocks for internal methods
        with patch.object(self.enricher, 'fetch_enrichment_data', new_callable=AsyncMock) as mock_fetch:
            with patch.object(self.enricher, 'process_response', new_callable=AsyncMock) as mock_process:
                # Mock rate limit then success
                mock_fetch.side_effect = fetch_results
                
                # Mock successful processing after retry
                expected_result = Artist('1', 'Test Artist', [Release('Test Release', 'Test Release', [], '2022-01-01', 'album', 10, 'https://spotify.com')])
                mock_process.return_value = expected_result
                
                # Run the method
                result = await self.enricher.enrich_artist_with_retries(mock_semaphore, mock_enrichment_source, artist)
                
                # Assertions
                assert result == expected_result
                assert mock_fetch.call_count == 2
                mock_process.assert_called_once_with({'name': 'Test Release'}, artist)
                # Should sleep based on retry_after value plus jitter
                expected_sleep_time = 5 + 1.0  # retry_after + mocked jitter
                mock_sleep.assert_called_once_with(expected_sleep_time)

    @patch('asyncio.sleep', new_callable=AsyncMock)
    @patch('random.uniform', return_value=1.0)  # Simplify jitter for testing
    async def test_enrich_artist_max_retries_exceeded(self, mock_uniform, mock_sleep):
        # Setup test data
        artist = Artist('1', 'Test Artist', [Release('Test Release', 'Test Release', [], None, None, None, None)])
        mock_semaphore = AsyncMock()
        mock_enrichment_source = AsyncMock()
        
        # Create side effects that always raise RateLimitError
        rate_limit_error = RateLimitError("Rate limit hit")
        
        # Setup mocks for internal methods
        with patch.object(self.enricher, 'fetch_enrichment_data', new_callable=AsyncMock) as mock_fetch:
            # Always hit rate limit
            mock_fetch.side_effect = rate_limit_error
            
            # Run the method
            result = await self.enricher.enrich_artist_with_retries(mock_semaphore, mock_enrichment_source, artist)
            
            # Assertions
            assert result == artist  # Should return original artist on failure
            assert mock_fetch.call_count == self.enricher.MAX_RETRIES + 1
            assert mock_sleep.call_count == self.enricher.MAX_RETRIES

    async def test_fetch_enrichment_data_with_missing_date(self):
        # Test data
        artist = Artist('1', 'Test Artist', [
            Release('Test Release 1', 'Test Release 1', [], None, None, None, None),  # Missing date
            Release('Test Release 2', 'Test Release 2', [], '2022-01-01', None, None, None)  # Has date
        ])
        
        mock_enrichment_source = AsyncMock()
        album_data = {'name': 'Test Album'}
        mock_enrichment_source.get_album.return_value = album_data
        
        # Use patch to intercept the call and verify it's happening correctly
        with patch.object(mock_enrichment_source, 'get_album', return_value=album_data) as mock_get_album:
            # Call the method
            result = await Enricher.fetch_enrichment_data(mock_enrichment_source, artist)
            
            # Assertions
            assert result == album_data
            mock_get_album.assert_called_once_with('Test Artist', 'Test Release 1')

    async def test_fetch_enrichment_data_with_no_missing_dates(self):
        # Test data
        artist = Artist('1', 'Test Artist', [
            Release('Test Release 1', 'Test Release 1', [], '2022-01-01', None, None, None),  # Has date
            Release('Test Release 2', 'Test Release 2', [], '2022-02-01', None, None, None)   # Has date
        ])
        mock_enrichment_source = AsyncMock()
        
        # Call the method
        result = await Enricher.fetch_enrichment_data(mock_enrichment_source, artist)
        
        # Assertions
        assert result == {}
        mock_enrichment_source.get_album.assert_not_called()

    async def test_process_response(self):
        # Test data
        artist = Artist('1', 'Test Artist', [
            Release('Test Release', 'Test Release', [], None, None, None, None)
        ])
        album_data = {'name': 'Test Album'}
        
        # Setup mock source class and enricher
        mock_source = Mock()
        enricher = Enricher(mock_source)
        
        # Setup mock release details
        release_details = ExternalRelease(
            name='Test Release',
            artist='Test Artist',
            date='2022-01-01',
            type='album',
            total_tracks=10,
            spotify_url='https://spotify.com'
        )
        
        # Mock the get_release_from_album method
        mock_source.get_release_from_album = AsyncMock(return_value=release_details)
        
        # Call the method
        result = await enricher.process_response(album_data, artist)
        
        # Assertions
        assert result.releases[0].name == 'Test Release'
        assert result.releases[0].date == '2022-01-01'
        assert result.releases[0].type == 'album'
        assert result.releases[0].total_tracks == 10
        assert result.releases[0].spotify_url == 'https://spotify.com'
        mock_source.get_release_from_album.assert_called_once_with(album_data, artist)


if __name__ == '__main__':
    unittest.main()