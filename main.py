import requests
import eel
import os
import youtube_dl

OAUTH_TOKEN = "YOUR_OAUTH_TOKEN_HERE"
BLOCK_REQUESTS = False
DOWNLOAD_DIRECTORY = "downloads"

def get_id_from_token(token):
    parts = token.split('-')
    return parts[2] if len(parts) > 2 else None

user_id = get_id_from_token(OAUTH_TOKEN)
original_url = f"https://api-v2.soundcloud.com/users/{user_id}/track_likes"
next_href = original_url

ydl_opts_info = {
    "quiet": True,
    "skip_download": True,
}

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US;q=0.8,en;q=0.7",
    "authorization": f"OAuth {OAUTH_TOKEN}",
}

@eel.expose
def get_tracks() -> dict:
    global BLOCK_REQUESTS, next_href

    if BLOCK_REQUESTS:
        return {}

    try:
        response = requests.get(next_href, headers=headers)
        response.raise_for_status()

        if next_href == original_url:
            eel.createNotification("Loading tracks", "Some images may not load", "/img/logo.png")
        
        next_href = response.json().get("next_href")
        return response.json().get("collection", {})
    
    except requests.HTTPError as http_err:
        if response.status_code == 401:
            BLOCK_REQUESTS = True
            eel.createNotification("Invalid Token", "Fix your token to work!", "/img/logo.png")
            print("Invalid token!")
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return {}

@eel.expose
def download_track(url):
    if not os.path.exists(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)

    if track_exists(url):
        eel.createNotification("Download Aborted", "The file already exists.", "/img/logo.png")
        return False

    try:
        with youtube_dl.YoutubeDL(ydl_opts_info) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get("title", None)
            filename = os.path.join(DOWNLOAD_DIRECTORY, f"{title}.mp3")

        eel.createNotification("Download Started", "The download has started.", "/img/downloading.png")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": filename,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        eel.createNotification("Download Complete", "The file has been downloaded successfully.", "/img/downloaded.png")
        return True

    except Exception as e:
        eel.createNotification("Download Failed", "An error occurred during the download.", "/img/logo.png")
        print(f"Error during download: {e}")
        return False

@eel.expose
def track_exists(track_name):
    filename = os.path.join(DOWNLOAD_DIRECTORY, f"{track_name}.mp3")
    return os.path.isfile(filename)

@eel.expose
def create_notification(title, description, img):
    eel.createNotification(title, description, img)

@eel.expose
def set_original_url():
    global next_href
    next_href = original_url

if __name__ == "__main__":
    print("SoundCloud Downloader")
    print("Made by slx10")
    print("\nMy socials")
    print("Github > slx10")
    print("Discord > slx.10\n")

    eel.init("web")
    eel.start("home.html", size=(1920, 1080), mode="chrome")
