import gradio as gr
import webbrowser
import yt_dlp
import os
from config import config


# -------------------------- 仅新增：ffmpeg 路径配置（不影响界面） --------------------------
def get_ffmpeg_path():
    """自动获取同级目录下的 ffmpeg 路径（适配 Windows/Mac/Linux）"""
    ffmpeg_bin_dir = config["FFMPEG_PATH"]
    if os.name == "nt":  # Windows 系统（带 .exe 后缀）
        ffmpeg_path = os.path.join(ffmpeg_bin_dir, "ffmpeg.exe")
        ffprobe_path = os.path.join(ffmpeg_bin_dir, "ffprobe.exe")
    else:  # Mac/Linux 系统（无 .exe 后缀）
        ffmpeg_path = os.path.join(ffmpeg_bin_dir, "ffmpeg")
        ffprobe_path = os.path.join(ffmpeg_bin_dir, "ffprobe")

    # 验证 ffmpeg 是否存在，不存在则报错提示
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(
            f"FFmpeg not found! Check path: {ffmpeg_path}\n"
            "Solution:\n1. Download static build from https://ffmpeg.org/download.html\n"
            "2. Extract and place ffmpeg.exe/ffprobe.exe in project's ffmpeg/bin folder"
        )
    return ffmpeg_path, ffprobe_path


# 预加载 ffmpeg 路径（启动时验证，不影响界面）
FFMPEG_PATH, FFPROBE_PATH = get_ffmpeg_path()


# -------------------------- 原有下载函数：优化网络请求 + ffmpeg 配置 + 同名拒绝下载 --------------------------
def download_video(video_url, noplaylist, save_path):
    # confirm the save_path exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        # config yt-dlp（一次性配置所有选项）
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # the best quality
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Output Template
            'noplaylist': noplaylist,  # By default, only download a single video, not the playlist.
            'quiet': False,  # Display download progress.
            'progress': True,  # Display progress bar.
            'geo-bypass': True,  # Bypass geo-restrictions (if any).
            # 指定 ffmpeg 路径（解决依赖问题）
            'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
            'ffprobe_location': FFPROBE_PATH,
            'overwrites': False,  # 强制关闭覆盖，双重保障
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }

        # Add proxy if it exists and is not None（只在需要时添加代理）
        if config.get('PROXY'):
            ydl_opts['proxy'] = config['PROXY']

        # 使用同一个 ydl 对象：先获取信息检查文件，再下载（避免重复请求）
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息，判断文件是否已存在
            info = ydl.extract_info(video_url, download=False)
            video_title = info.get('title', 'video')
            ext = info.get('ext', 'mp4')

            # 生成最终文件名（和下载后一致）
            final_filename = f"{video_title}.{ext}"
            final_file_path = os.path.join(save_path, final_filename)

            # 关键：同名文件直接拒绝下载
            if os.path.exists(final_file_path):
                return {
                    'status': 'error',
                    'message': f'File already exists! Rejected download.\nPath: {final_file_path}',
                    'error': 'Duplicate file'
                }

            # 文件不存在，开始下载（复用已获取的 info，不会重复请求）
            ydl.process_info(info)

        return {
            'status': 'success',
            'message': f'Video "{video_title}" Download complete.',
            'title': video_title,
            'path': save_path
        }

    except FileNotFoundError as e:
        # 捕获 ffmpeg 未找到的错误
        return {
            'status': 'error',
            'message': f'Download failed: {str(e)}',
            'error': str(e)
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Download failed: {str(e)}',
            'error': str(e)
        }


# -------------------------- 原有界面处理函数：完全不变 --------------------------
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


# -------------------------- 原有界面：完全不变（保留你的原始样式） --------------------------
iface = gr.Interface(
    fn=interface_download,
    inputs=[
        gr.Textbox(label="Video link", placeholder="Please enter the video link...", lines=2),
        gr.Radio(["Single video", "Entire playlist"], label="Select download option", value="Single video"),
        gr.Textbox(label="Save path", placeholder=config['DIR'], value=config['DIR'],lines=2)
    ],
    outputs=gr.Textbox(label="Download status", lines=10),
    title="Video downloader",
    description="Enter the video link and save path, then click submit to start the download.",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    webbrowser.open("http://localhost:7860/")
    iface.launch(share=False)
