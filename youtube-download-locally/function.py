import yt_dlp
import os

import constant


def download_video(url, output_path=constant.Constant.DIR):
    """
    使用yt-dlp下载视频

    Args:
        url (str): 视频链接
        output_path (str): 下载保存路径

    Returns:
        dict: 包含下载状态和信息的字典
    """
    try:
        # 确保输出路径存在
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # 配置yt-dlp选项
        ydl_opts = {
            'format': 'best',  # 下载最佳质量
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # 输出模板
            'quiet': False,  # 显示下载进度
            'progress': True,  # 显示进度条
            'proxy': constant.Constant.PROXY,
        }

        # 获取视频信息
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', None)

            # 开始下载
            ydl.download([url])

        return {
            'status': 'success',
            'message': f'视频 "{video_title}" 下载完成',
            'title': video_title,
            'path': output_path
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'下载失败: {str(e)}',
            'error': str(e)
        }
