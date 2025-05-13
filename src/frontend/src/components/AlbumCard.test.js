import React from 'react';
import { render, screen } from '@testing-library/react';
import AlbumCard from './AlbumCard';

describe('AlbumCard', () => {
  // Default album with all properties
  const defaultAlbum = {
    release_name: 'Test Album',
    artist_name: 'Test Artist',
    score: 85,
    user_score: 75,
    date: '2023-01-15',
    reviews_counted: 10,
    cover_url: 'https://example.com/test-album.jpg'
  };

  test('renders album with cover URL from backend', () => {
    render(<AlbumCard album={defaultAlbum} />);
    
    const coverImage = screen.getByAltText('Test Album');
    expect(coverImage).toBeInTheDocument();
    expect(coverImage.src).toBe('https://example.com/test-album.jpg');
  });

  test('renders album with default cover when cover_url is missing', () => {
    const albumWithoutCover = {
      ...defaultAlbum,
      cover_url: null
    };
    
    render(<AlbumCard album={albumWithoutCover} />);
    
    const coverImage = screen.getByAltText('Test Album');
    expect(coverImage).toBeInTheDocument();
    expect(coverImage.src).toBe('https://f4.bcbits.com/img/a1091823768_10.jpg');
  });

  test('renders album with default cover when cover_url is empty string', () => {
    const albumWithEmptyCover = {
      ...defaultAlbum,
      cover_url: ''
    };
    
    render(<AlbumCard album={albumWithEmptyCover} />);
    
    const coverImage = screen.getByAltText('Test Album');
    expect(coverImage).toBeInTheDocument();
    expect(coverImage.src).toBe('https://f4.bcbits.com/img/a1091823768_10.jpg');
  });

  test('renders album with correct score styling based on critic score', () => {
    // Fresh score (75+)
    render(<AlbumCard album={{...defaultAlbum, score: 90}} />);
    expect(screen.getByText('90%')).toHaveClass('score-fresh');
    
    // Mixed score (60-74)
    render(<AlbumCard album={{...defaultAlbum, score: 65}} />);
    expect(screen.getByText('65%')).toHaveClass('score-mixed');
    
    // Rotten score (<60)
    render(<AlbumCard album={{...defaultAlbum, score: 45}} />);
    expect(screen.getByText('45%')).toHaveClass('score-rotten');
  });

  test('renders album with all expected information', () => {
    render(<AlbumCard album={defaultAlbum} />);
    
    // Check all displayed information
    expect(screen.getByText('Test Album')).toBeInTheDocument();
    expect(screen.getByText('Test Artist')).toBeInTheDocument();
    expect(screen.getByText('85%')).toBeInTheDocument();
    expect(screen.getByText('75%')).toBeInTheDocument();
    expect(screen.getByText('2023')).toBeInTheDocument();
    expect(screen.getByText('10 reviews')).toBeInTheDocument();
  });
}); 