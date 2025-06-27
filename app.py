import gradio as gr
import webbrowser
import yt_dlp
import os
from config import config


def download_video(video_url, noplaylist, save_path):
    # confirm the save_path exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        # config yt-dlp
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # the best quality
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Output Template
            'noplaylist': noplaylist,  # By default, only download a single video, not the playlist.
            'quiet': False,  # Display download progress.
            'progress': True,  # Display progress bar.
            'geo-bypass': True,  # Bypass geo-restrictions (if any).
        }

        # Add proxy if it exists in config
        if 'PROXY' in config:
            ydl_opts['proxy'] = config['PROXY']

        # Fetch video information.
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_title = info.get('title', None)

            # Start download.
            ydl.download([video_url])

        return {
            'status': 'success',
            'message': f'Video "{video_title}" Download complete.',
            'title': video_title,
            'path': save_path
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Download failed: {str(e)}',
            'error': str(e)
        }


def interface_download(video_url, noplaylist, save_path):
    """
    Gradio interface handler function.
    """
    if not video_url:
        return "Please enter the video link!"

    # Update the noplaylist parameter based on the selected download option.
    noplaylist = True if noplaylist == "Single video" else False

    if not save_path:
        save_path = config['DIR']

    # Call the download function
    result = download_video(video_url, noplaylist, save_path)

    if result['status'] == 'success':
        return f"✅ {result['message']}\nSave location: {result['path']}"
    else:
        return f"❌ {result['message']}"


# Create Gradio interface
iface = gr.Interface(
    fn=interface_download,
    inputs=[
        gr.Textbox(label="Video link", placeholder="Please enter the video link..."),
        gr.Radio(["Single video", "Entire playlist"], label="Select download option", value="Single video"),
        gr.Textbox(label="Save path", placeholder=config['DIR'], value=config['DIR'])
    ],
    outputs=gr.Textbox(label="Download status"),
    title="Video downloader",
    description="Enter the video link and save path, then click submit to start the download.",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    webbrowser.open("http://localhost:7860/")
    iface.launch(share=False)
