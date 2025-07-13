from flask import Flask, render_template, request, send_from_directory
import os
from pytube import YouTube
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        try:
            yt = YouTube(youtube_url)
            video_title = yt.title
            # Create a safe filename
            safe_title = "".join(c for c in video_title if c.isalnum() or c in " -_")
            filename = f"{safe_title}.mp3"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Download the audio stream
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=app.config['UPLOAD_FOLDER'], filename=filename)
            
            # Return the file for download
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
    app.run(debug=True)
