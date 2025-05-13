# Ripe Peaches Frontend

This is the React frontend for the Ripe Peaches application, which aggregates album reviews similarly to how Rotten Tomatoes aggregates movie reviews.

## Features

- Displays album scores and information in a grid layout
- Allows sorting by score, release date, and album name
- Uses a visual system similar to Rotten Tomatoes with "fresh" and "rotten" scores
- Responsive design for mobile and desktop viewing

## Getting Started

1. Make sure the backend server is running on port 8888
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```
4. Open [http://localhost:3000](http://localhost:3000) to view the app in your browser

## Implementation Notes

- The frontend uses placeholder images for album covers
- The app will fetch data from the `/` endpoint of the backend
- Color coding follows Rotten Tomatoes style:
  - Green (75%+): Fresh
  - Yellow (60-74%): Mixed
  - Red (below 60%): Rotten 