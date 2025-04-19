import os
from pytubefix import YouTube  # Updated import
from moviepy.video.io.VideoFileClip import VideoFileClip


#While pytubefix worked, yt-dlp is another robust alternative that’s even more actively maintained. If you face issues with pytubefix in the future, consider switching:


def download_video_and_extract_audio(url):
    try:
        # If you encounter videos that are age-restricted or region-locked, you can enable OAuth
        # yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not video:
            print("No suitable video stream found.")
            return
        
        print(f"Downloading: {yt.title}")
        video_path = video.download()
        print("Video downloaded successfully!")

        video_clip = VideoFileClip(video_path)
        audio_path = os.path.splitext(video_path)[0] + '.mp3'
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
        os.remove(video_path)
        print(f"Audio extracted to: {audio_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    download_video_and_extract_audio(url)