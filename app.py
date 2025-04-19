import os
from flask import Flask, render_template, request, send_file, jsonify
from pytubefix import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)

# Ensure the downloads directory exists
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        if not url:
            return jsonify({"error": "Please provide a YouTube URL"}), 400

        # Download video
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not video:
            return jsonify({"error": "No suitable video stream found"}), 400

        video_path = video.download(output_path=DOWNLOAD_FOLDER)
        
        # Extract audio
        video_clip = VideoFileClip(video_path)
        audio_path = os.path.splitext(video_path)[0] + '.mp3'
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()

        # Clean up video file (optional, if you only need the MP3)
        os.remove(video_path)

        # Return the path to the MP3 file for download
        return jsonify({"success": True, "audio_path": audio_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download_file/<path:filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)