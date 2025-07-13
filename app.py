from flask import Flask, render_template, request, send_from_directory
import os
import re
import uuid
from urllib.parse import quote as url_quote
from werkzeug.utils import secure_filename
import yt_dlp as youtube_dl  # More reliable library

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit

# Create downloads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        
        # Validate YouTube URL
        if not youtube_url or 'youtube.com/' not in youtube_url and 'youtu.be/' not in youtube_url:
            return render_template('index.html', error="Please enter a valid YouTube URL")
        
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(title)s.%(ext)s'),
                'quiet': True,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                filename = sanitize_filename(f"{info['title']}.mp3")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Rename file to ensure .mp3 extension
                temp_path = filepath.replace('.mp3', '') + '.mp3'
                if os.path.exists(temp_path):
                    os.rename(temp_path, filepath)

            return send_from_directory(
                app.config['UPLOAD_FOLDER'],
                filename,
                as_attachment=True,
                mimetype='audio/mpeg'
            )
            
        except Exception as e:
            error_msg = f"Error downloading video: {str(e)}"
            if "Unsupported URL" in str(e):
                error_msg = "This YouTube URL is not supported. Try a different video."
            return render_template('index.html', error=error_msg)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
