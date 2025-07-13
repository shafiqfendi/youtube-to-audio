from flask import Flask, render_template, request, send_from_directory
import os
from pytube import YouTube
import uuid
from werkzeug.utils import secure_filename
from urllib.parse import quote as url_quote

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit

# Create downloads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        try:
            yt = YouTube(youtube_url)
            video_title = "".join(c for c in yt.title if c.isalnum() or c in " -_")
            filename = secure_filename(f"{video_title}.mp3")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Download audio
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=app.config['UPLOAD_FOLDER'], filename=filename)
            
            return send_from_directory(
                app.config['UPLOAD_FOLDER'],
                filename,
                as_attachment=True,
                mimetype='audio/mpeg'
            )
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
