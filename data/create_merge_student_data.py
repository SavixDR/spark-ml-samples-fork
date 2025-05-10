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

# Containers for classic genre
classic_artists = []
classic_tracks = []
classic_years = []
classic_genres = []
classic_lyrics = []

i = 1

# Fetch classic tracks from Spotify
for offset in range(0, 500, 50):
    classic_results = spotify_client.search(q="genre:classic", type="track", limit=50, offset=offset)

    for track in classic_results["tracks"]["items"]:
        try:
            print(f"Processing {i}: {track['name']} by {track['artists'][0]['name']}")
            i += 1

            song = genius_client.search_song(track["name"], track["artists"][0]["name"])
            if not song:
                continue

            lyrics_text = song.lyrics
            lyrics_text = re.sub(r"^.*?\n+", "", lyrics_text, count=1)
            lyrics_text = re.sub(r"\s+", " ", lyrics_text)

            classic_artists.append(track["artists"][0]["name"])
            classic_tracks.append(track["name"])
            classic_years.append(track["album"]["release_date"])
            classic_genres.append("classic")
            classic_lyrics.append(lyrics_text)

        except Exception as e:
            print(f"Error: {e}")
            continue

# Create DataFrame
classic_df = pd.DataFrame({
    "artist_name": classic_artists,
    "track_name": classic_tracks,
    "release_date": classic_years,
    "genre": classic_genres,
    "lyrics": classic_lyrics
})

# Format and clean data
classic_df["release_date"] = pd.to_datetime(classic_df["release_date"], errors="coerce")
classic_df.dropna(subset=["release_date"], inplace=True)
classic_df["release_date"] = classic_df["release_date"].dt.year.astype("int64")
classic_df.dropna(subset=["lyrics"], inplace=True)
classic_df.drop_duplicates(subset=["lyrics", "track_name"], inplace=True)
classic_df["lyrics"] = classic_df["lyrics"].apply(lambda x: re.sub(r"[^\x00-\x7F]+", "", x))
classic_df["lyrics"] = classic_df["lyrics"].str.replace(r"\[.*?\]", "", regex=True)

# Save classic dataset
classic_df.to_csv("data/Student_dataset.csv", index=False)

classic_df = pd.read_csv("data/Student_dataset.csv")

# Merge with Mendeley dataset
mendeley_df = pd.read_csv("data/Mendeley_dataset.csv")
mendeley_df = mendeley_df[["artist_name", "track_name", "release_date", "genre", "lyrics"]]
merged_df = pd.concat([mendeley_df, classic_df], ignore_index=True)

# Save merged dataset
merged_df.to_csv("data/Merged_dataset.csv", index=False)

print("✅ classic lyrics fetched and merged successfully.")

