import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import requests

client_id = "73d8939b2df341b49308c2705babd9e8"
client_secret = "0fac4b5ca15942c5ad44d57bbb37524d"
REDIRECT_URI = "http://localhost:8001"
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,client_secret,REDIRECT_URI,scope=scope))

results = sp.current_user_saved_tracks(limit=50)
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])


# Get the user's saved tracks
tracks = []
offset = 0
while True:
    results = sp.current_user_saved_tracks(limit=50, offset=offset)
    items = results["items"]
    tracks.extend(items)
    offset += len(items)
    if len(items) == 0:
        break

# Extract the relevant information and audio features for each track
track_info = []
for track in tracks:
    # Get the track information
    info = {
        "artist": track["track"]["artists"][0]["name"],
        "title": track["track"]["name"],
        "album": track["track"]["album"]["name"],
        "added_at": track["added_at"]
    }
    # Get the audio features for the track
    audio_features = sp.audio_features([track["track"]["id"]])[0]
    # Merge the track information and audio features into a single dictionary
    info.update(audio_features)
    track_info.append(info)

# Write the track information to a CSV file
with open("My_liked_songs_with_features.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["artist", "title", "album", "added_at", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "type", "id", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"])
    writer.writeheader()
    writer.writerows(track_info)


# Print the total number of tracks
print(f"Total number of tracks: {len(tracks)}")


