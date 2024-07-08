# SoundCloud Downloader

SoundCloud Downloader is a web application designed to download and manage your favorite tracks from SoundCloud. Built using Python, Eel, and JavaScript, this project allows you to fetch your liked tracks from SoundCloud, display them in a user-friendly interface, and download them with ease.

![Showcase](web/img/showcase.jpg)

## Features

- **Fetch Liked Tracks**: Retrieve your liked tracks from SoundCloud using your OAuth token.
- **Display Tracks**: Display track details including artwork, title, and author.
- **Download Tracks**: Download tracks directly to your local directory.
- **Track Existence Check**: Prevent duplicate downloads by checking if a track already exists.

> **Note**: FFmpeg is required to download and convert the audio files. Make sure you have FFmpeg installed and configured in your system's PATH.

## Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/slx10/soundcloud-downloader.git
   cd soundcloud-downloader
   ```

2. **Install the required Python packages**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up your OAuth token**
   Replace the placeholder `OAUTH_TOKEN` in `app.py` with your actual SoundCloud OAuth token.
   ```python
   OAUTH_TOKEN = "YOUR_OAUTH_TOKEN_HERE"
   ```

4. **Run the application**
   ```sh
   python app.py
   ```