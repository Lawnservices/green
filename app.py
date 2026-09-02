import os
import requests
from flask import Flask, render_template, redirect

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

YOUTUBE_CHANNEL_ID = "UCvAAQ-XjDtww6RWLmltErCw"


def obtener_videos_youtube(max_results=20):

    if not YOUTUBE_API_KEY:
        print("ERROR: YOUTUBE_API_KEY is not configured")
        return []

    # ==========================================
    # 1. GET UPLOADS PLAYLIST
    # ==========================================

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
        print("YOUTUBE CHANNEL ERROR")
        print(channel_response.status_code)
        print(channel_response.text)
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


    # ==========================================
    # 2. GET VIDEOS
    # ==========================================

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

    if playlist_response.status_code != 200:
        print("YOUTUBE PLAYLIST ERROR")
        print(playlist_response.status_code)
        print(playlist_response.text)
        return []

    playlist_data = playlist_response.json()


    # ==========================================
    # 3. CREATE VIDEO LIST
    # ==========================================

    videos = []

    for item in playlist_data.get("items", []):

        video_id = item["contentDetails"]["videoId"]
        snippet = item["snippet"]

        videos.append({
            "id": video_id,
            "title": snippet["title"],
            "description": snippet["description"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "published_at": snippet["publishedAt"],
            "views": 0
        })


    # ==========================================
    # 4. GET VIEW COUNTS
    # ==========================================

    if videos:

        video_ids = ",".join(
            video["id"] for video in videos
        )

        stats_url = "https://www.googleapis.com/youtube/v3/videos"

        stats_params = {
            "part": "statistics",
            "id": video_ids,
            "key": YOUTUBE_API_KEY
        }

        stats_response = requests.get(
            stats_url,
            params=stats_params,
            timeout=10
        )

        if stats_response.status_code == 200:

            stats_data = stats_response.json()

            view_counts = {}

            for item in stats_data.get("items", []):

                video_id = item["id"]

                views = item.get(
                    "statistics",
                    {}
                ).get(
                    "viewCount",
                    "0"
                )

                view_counts[video_id] = views


            # Add views to each video
            for video in videos:

                video["views"] = view_counts.get(
                    video["id"],
                    "0"
                )


    return videos


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/prices")
def prices():
    return render_template("prices.html")


@app.route("/photos")
def photos():
    return render_template("photos.html")


@app.route("/videos")
def videos():

    youtube_videos = obtener_videos_youtube(20)

    return render_template(
        "videos.html",
        videos=youtube_videos
    )


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return redirect("/photos")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)