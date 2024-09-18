import yt_dlp
import os
from tqdm import tqdm

# Set the download location to the Download folder in internal storage
download_folder = '/storage/emulated/0/Download'

# Progress bar using tqdm
def progress_hook(d):
    if d['status'] == 'downloading':
        pbar.total = d.get('total_bytes', 0)
        pbar.update(d.get('downloaded_bytes', 0) - pbar.n)
        
    elif d['status'] == 'finished':
        pbar.close()
        print("\nDownload complete!")

# Ask the user for the playlist URL
playlist_url = input("Enter the YouTube playlist URL: ")

# Ask the user for the desired quality
print("\nSelect the quality:")
print("1. Best quality (video + audio)")
print("2. Specific resolution (e.g., 720p, 1080p)")

quality_choice = input("Enter your choice (1 or 2): ")

if quality_choice == '1':
    video_format = 'bestvideo+bestaudio/best'
elif quality_choice == '2':
    resolution = input("Enter the resolution (e.g., 720p, 1080p): ")
    video_format = f"bestvideo[height<={resolution}]+bestaudio/best"
else:
    print("Invalid choice, defaulting to best quality.")
    video_format = 'bestvideo+bestaudio/best'

# Options for yt-dlp
ydl_opts = {
    'outtmpl': os.path.join(download_folder, '%(playlist)s/%(title)s.%(ext)s'),  # Save videos in a subfolder with the playlist name
    'format': video_format,  # Set video format based on user choice
    'merge_output_format': 'mp4',  # Ensure the output is MP4 after merging
    'ffmpeg_location': '/data/data/com.termux/files/usr/bin/ffmpeg',  # Path to ffmpeg
    'progress_hooks': [progress_hook],  # Attach the progress hook
    'noplaylist': False,  # Ensure the entire playlist is downloaded
}

# Initialize tqdm progress bar
pbar = tqdm(total=0, unit='B', unit_scale=True, unit_divisor=1024)

# Download the playlist
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])
