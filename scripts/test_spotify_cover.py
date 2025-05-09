import asyncio
import aiohttp
from src.collector.web.spotify import Spotify

async def fetch_and_print_cover(artist_name, album_name):
    async with aiohttp.ClientSession() as session:
        spotify = Spotify(session)
        search_result = await spotify.search_by_album_and_artist(artist_name, album_name)
        items = search_result.get('albums', {}).get('items', []) if search_result else []
        print(f"Found {len(items)} albums in search results.")
        for album in items:
            print(f"Album: {album.get('name')} | Artist(s): {[a['name'] for a in album.get('artists')]} | Type: {album.get('album_type')}")
        album_id = None
        for album in items:
            if (
                album.get('name', '').lower() == album_name.lower() and
                any(a['name'].lower() == artist_name.lower() for a in album.get('artists')) and
                album.get('album_type') == 'album'
            ):
                album_id = album['id']
                break
        if album_id:
            album_details = await spotify.get_album_details(album_id)
            images = album_details.get('images', []) if album_details else []
            if images:
                print("Highest-res cover art URL:", images[0]['url'])
            else:
                print("No cover art found in album details.")
        else:
            print("No matching album found.")

if __name__ == "__main__":
    # Example: Black Sabbath - Paranoid
    asyncio.run(fetch_and_print_cover("Black Sabbath", "Paranoid")) 