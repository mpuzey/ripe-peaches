import React, { useState, useEffect } from 'react';
import AlbumList from './components/AlbumList';
import './App.css';

function App() {
  const [albums, setAlbums] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('score');

  useEffect(() => {
    fetchAlbums();
  }, []);

  const fetchAlbums = async () => {
    try {
      const response = await fetch('http://localhost:8888/', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        mode: 'cors'
      });
      
      const data = await response.json();
      console.log('Received data:', data);
      
      if (data && data.scores) {
        setAlbums(Object.values(data.scores));
      } else {
        console.error('Unexpected data format:', data);
        setAlbums([]);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching album data:', error);
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header app-header-left">
        <div className="logo-and-tagline">
          <div className="logo-circle">
            <img src="/images/ripe-peaches-logo.png" alt="Ripe Peaches Logo" className="peach-logo-huge" />
          </div>
          <div className="tagline">Fresh Music Reviews</div>
        </div>
      </header>
      <div className="container">
        <div className="filter-section">
          <h2>Best Albums (2025)</h2>
          <div className="sort-controls">
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="score">Sort: Highest Rated</option>
              <option value="date">Sort: Release Date</option>
              <option value="name">Sort: Album Name</option>
            </select>
          </div>
        </div>
        {loading ? (
          <div className="loading">Loading albums...</div>
        ) : (
          <AlbumList albums={albums} sortBy={sortBy} />
        )}
      </div>
    </div>
  );
}

export default App; 