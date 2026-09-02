import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prices')
def prices():
    return render_template('prices.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# nuevo 
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

#YOUTUBE_API_KEY = "AIzaSyA7EwPFyuZEGId8om24B0y1AFaC-vy8vVs"
# ID de tu canal de YouTube
YOUTUBE_CHANNEL_ID = "UCvAAQ-XjDtww6RWLmltErCw"


def obtener_videos_youtube(max_results=20):

    # 1. Obtener el Uploads Playlist ID
    channel_url = "https://www.googleapis.com/youtube/v3/channels"

    channel_params = {
        "part": "contentDetails",
        "key": YOUTUBE_API_KEY,
        "id": YOUTUBE_CHANNEL_ID
        
    }

    channel_response = requests.get(
        channel_url,
        params=channel_params,
        timeout=10
    )

    if channel_response.status_code != 200:
         print("ERROR DE YOUTUBE")
         print("CODIGO:", channel_response.status_code)
         print("RESPUESTA:", channel_response.text)
         return []
        

    channel_data = channel_response.json()

    if not channel_data.get("items"):
        return []

    uploads_playlist_id = (
        channel_data["items"][0]
        ["contentDetails"]
        ["relatedPlaylists"]
        ["uploads"]
    )

    # 2. Obtener los videos
    playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"

    playlist_params = {
        "part": "snippet,contentDetails",
        "playlistId": uploads_playlist_id,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    playlist_response = requests.get(
        playlist_url,
        params=playlist_params,
        timeout=10
    )

    playlist_response.raise_for_status()

    playlist_data = playlist_response.json()

    videos = []

    for item in playlist_data.get("items", []):

        video_id = item["contentDetails"]["videoId"]
        snippet = item["snippet"]

        videos.append({
            "id": video_id,
            "title": snippet["title"],
            "description": snippet["description"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "published_at": snippet["publishedAt"]
        })

    return videos


# ==========================================
# PÁGINA DE VIDEOS
# ==========================================

@app.route("/videos")
def videos():

    youtube_videos = obtener_videos_youtube(20)

    return render_template(
        "videos.html",
        videos=youtube_videos
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)