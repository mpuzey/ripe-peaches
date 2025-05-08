import React from 'react';
import './AlbumCard.css';

function AlbumCard({ album }) {
  // Generate placeholder album cover
  const albumName = album.release_name || 'Unknown Album';
  const artistName = album.artist_name || 'Unknown Artist';
  
  const placeholderCover = `https://via.placeholder.com/200x200/333333/ffffff?text=${encodeURIComponent(albumName)}`;
  
  // Format date to show just the year
  const releaseYear = album.date ? new Date(album.date).getFullYear() : 'Unknown';
  
  // Calculate critic score color class (similar to Rotten Tomatoes)
  const getScoreColorClass = (score) => {
    if (score >= 75) return 'score-fresh';
    if (score >= 60) return 'score-mixed';
    return 'score-rotten';
  };

  // Calculate audience score color class
  const getUserScoreColorClass = (score) => {
    if (score >= 70) return 'score-fresh';
    if (score >= 50) return 'score-mixed';
    return 'score-rotten';
  };

  return (
    <div className="album-card">
      <div className="album-cover">
        <img src={placeholderCover} alt={albumName} />
      </div>
      <div className="album-info">
        <div className={`score ${getScoreColorClass(album.score || 0)}`}>
          {Math.round(album.score || 0)}%
        </div>
        {album.user_score && (
          <div className={`user-score ${getUserScoreColorClass(album.user_score || 0)}`}>
            {Math.round(album.user_score || 0)}%
          </div>
        )}
        <h3 className="album-title">{albumName}</h3>
        <div className="album-artist">{artistName}</div>
        <div className="album-year">{releaseYear}</div>
        <div className="album-reviews">{album.reviews_counted || 0} reviews</div>
      </div>
    </div>
  );
}

export default AlbumCard; 