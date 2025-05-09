import React, { useMemo } from 'react';
import AlbumCard from './AlbumCard';
import './AlbumList.css';

function AlbumList({ albums, sortBy }) {
  const sortedAlbums = useMemo(() => {
    if (!albums || !albums.length) return [];
    
    return [...albums].sort((a, b) => {
      if (sortBy === 'score') {
        return (b.score || 0) - (a.score || 0);
      } else if (sortBy === 'date') {
        const dateA = a.date ? new Date(a.date) : new Date(0);
        const dateB = b.date ? new Date(b.date) : new Date(0);
        return dateB - dateA;
      } else if (sortBy === 'name') {
        const nameA = a.release_name || '';
        const nameB = b.release_name || '';
        return nameA.localeCompare(nameB);
      }
      return 0;
    });
  }, [albums, sortBy]);

  if (!sortedAlbums.length) {
    return <div className="no-albums">No albums found</div>;
  }

  return (
    <div className="album-list">
      {sortedAlbums.map((album, index) => (
        <AlbumCard key={album.id || index} album={album} />
      ))}
    </div>
  );
}

export default AlbumList; 