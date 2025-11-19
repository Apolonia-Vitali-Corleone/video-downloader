# Video Downloader

A modern web-based video downloader with support for YouTube, TikTok, Bilibili, Pornhub and hundreds of other platforms powered by yt-dlp.

## Features

- 🌐 **Web Interface** - User-friendly GUI, no command-line knowledge required
- 🚀 **High Quality** - Automatically downloads best available video and audio quality
- 🔄 **Smart Downloads** - Duplicate detection prevents re-downloading existing files
- 🌍 **Proxy Support** - Configure proxy for geo-restricted content
- 📋 **Playlist Support** - Download entire playlists with a single click
- 💻 **Cross-Platform** - Works on Windows, macOS, and Linux

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

FFmpeg is required for video processing and merging.

1. Download FFmpeg static binaries from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the downloaded archive
3. Copy the following executables to `./ffmpeg/bin/` directory:
   - `ffmpeg` (or `ffmpeg.exe` on Windows)
   - `ffprobe` (or `ffprobe.exe` on Windows)
   - `ffplay` (or `ffplay.exe` on Windows)

### 3. Configure Settings

Edit `config.py` to customize your download directory and proxy settings:

```python
config = {
    # Download directory (use raw string r"" to avoid path escape issues)
    'DIR': r"D:\Video",

    # Proxy configuration (set to None if not using a proxy)
    'PROXY': 'http://127.0.0.1:7890',  # or None

    # FFmpeg binary path
    'FFMPEG_PATH': os.path.join(".", "ffmpeg", "bin")
}
```

## Usage

### Start the Application

**Windows:** Double-click `run.bat`

**macOS/Linux:** Run `bash run.sh` or `python app.py`

The web interface will automatically open in your browser at `http://localhost:7860/`

### Download Videos

1. Paste the video URL into the input field
2. Click the download button
3. Wait for the download to complete
4. Find your video in the configured download directory

## Configuration Guide

### Proxy Settings

#### For Users Behind Firewalls (e.g., Mainland China)

If you need a proxy to access certain video platforms, configure it in `config.py`:

```python
config = {
    'DIR': r"F:\Video",
    'PROXY': 'http://127.0.0.1:4343',  # Your proxy server address
    'FFMPEG_PATH': os.path.join(".", "ffmpeg", "bin")
}
```

#### For International Users

If you have direct access to video platforms, disable the proxy:

```python
config = {
    'DIR': r"F:\Video",
    'PROXY': None,  # No proxy needed
    'FFMPEG_PATH': os.path.join(".", "ffmpeg", "bin")
}
```

### Download Directory

Specify your preferred download location using an absolute path:

- **Windows:** `r"D:\Videos\Downloads"`
- **macOS/Linux:** `"/home/username/Videos"` or `"~/Videos"`

*Note: Use raw strings (r"") on Windows to avoid backslash escape issues*

## Supported Platforms

### Verified Platforms

- ✅ YouTube
- ✅ TikTok
- ✅ Bilibili
- ✅ Pornhub

### Additional Platforms

This tool supports **1000+ video platforms** through yt-dlp. For a complete list, see [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Troubleshooting

### FFmpeg Not Found

Ensure FFmpeg executables are placed in `./ffmpeg/bin/` directory and the path is correctly configured in `config.py`.

### Download Fails

- Check your internet connection
- Verify the video URL is valid and accessible
- If accessing geo-restricted content, ensure your proxy is configured correctly
- Some platforms may require authentication or have anti-bot protection

### Port Already in Use

If port 7860 is occupied, edit `app.py` to change the port number in the `app.launch()` call.

## License

This project is for educational and personal use only. Please respect video platform terms of service and copyright laws.

## Credits

Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [Gradio](https://gradio.app/).
