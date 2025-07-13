# YouTube to MP3 Converter (Auto-Download Version)

A simple web application that converts YouTube videos to MP3 files and automatically downloads them.

## How it Works

1. You enter a YouTube URL
2. The server processes the video and converts it to MP3
3. The MP3 file is automatically downloaded to your device
4. No intermediate pages - direct download

## Deployment to Render.com

1. Push this repository to GitHub
2. Create a new Web Service on Render.com
3. Connect your GitHub repository
4. Set the following configuration:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Deploy!
