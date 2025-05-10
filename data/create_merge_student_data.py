import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import pandas as pd
import re

# Spotify and Genius API credentials
SPOTIPY_CLIENT_ID = "95614d11af4546dbb08b90dcc67bcd34"
SPOTIPY_CLIENT_SECRET = "94809bebc2b54219a77a22aa2793e090"
GENIUS_CLIENT_ACCESS_TOKEN = "REYJhsHt3VW_kE16jDw0pYr5ywujdCmzVzDxoVKVC_Yg_xhao-vFIucwYD3cI79g"

# Initialize Spotify and Genius API clients
spotify_client = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
    ),
    requests_timeout=40
)

genius_client = lyricsgenius.Genius(GENIUS_CLIENT_ACCESS_TOKEN, timeout=40)

# Containers for electro genre
electro_artists = []
electro_tracks = []
electro_years = []
electro_genres = []
electro_lyrics = []

i = 1

# Fetch Electro tracks from Spotify
for offset in range(0, 200, 50):
    electro_results = spotify_client.search(q="genre:electro", type="track", limit=50, offset=offset)

    for track in electro_results["tracks"]["items"]:
        try:
            print(f"Processing {i}: {track['name']} by {track['artists'][0]['name']}")
            i += 1

            song = genius_client.search_song(track["name"], track["artists"][0]["name"])
            if not song:
                continue

            lyrics_text = song.lyrics
            lyrics_text = re.sub(r"^.*?\n+", "", lyrics_text, count=1)
            lyrics_text = re.sub(r"\s+", " ", lyrics_text)

            electro_artists.append(track["artists"][0]["name"])
            electro_tracks.append(track["name"])
            electro_years.append(track["album"]["release_date"])
            electro_genres.append("electro")
            electro_lyrics.append(lyrics_text)

        except Exception as e:
            print(f"Error: {e}")
            continue

# Create DataFrame
electro_df = pd.DataFrame({
    "artist_name": electro_artists,
    "track_name": electro_tracks,
    "release_date": electro_years,
    "genre": electro_genres,
    "lyrics": electro_lyrics
})

# Format and clean data
electro_df["release_date"] = pd.to_datetime(electro_df["release_date"], errors="coerce")
electro_df.dropna(subset=["release_date"], inplace=True)
electro_df["release_date"] = electro_df["release_date"].dt.year.astype("int64")
electro_df.dropna(subset=["lyrics"], inplace=True)
electro_df.drop_duplicates(subset=["lyrics", "track_name"], inplace=True)
electro_df["lyrics"] = electro_df["lyrics"].apply(lambda x: re.sub(r"[^\x00-\x7F]+", "", x))
electro_df["lyrics"] = electro_df["lyrics"].str.replace(r"\[.*?\]", "", regex=True)

# Save electro dataset
electro_df.to_csv("./Student_dataset.csv", index=False)

electro_df = pd.read_csv("data/Student_dataset.csv")

# Merge with Mendeley dataset
mendeley_df = pd.read_csv("data/Mendeley_dataset.csv")
mendeley_df = mendeley_df[["artist_name", "track_name", "release_date", "genre", "lyrics"]]
merged_df = pd.concat([mendeley_df, electro_df], ignore_index=True)

# Save merged dataset
merged_df.to_csv("Merged_dataset.csv", index=False)

print("✅ Electro lyrics fetched and merged successfully.")

