import gradio as gr
import webbrowser
import yt_dlp
import os
from config import config


def download_video(video_url, noplaylist, save_path):
    # 确保输出路径存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print("branch1")
    try:
        # 配置yt-dlp选项
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # 下载最佳质量
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # 输出模板
            'noplaylist': noplaylist,  # 默认只下载单个视频，不下载播放列表
            'quiet': False,  # 显示下载进度
            'progress': True,  # 显示进度条
            'geo-bypass': True,  # 绕过地理限制（如有）
            'proxy': config['PROXY'],  # 使用代理
        }

        # 获取视频信息
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_title = info.get('title', None)

            # 开始下载
            ydl.download([video_url])

        return {
            'status': 'success',
            'message': f'视频 "{video_title}" 下载完成',
            'title': video_title,
            'path': save_path
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'下载失败: {str(e)}',
            'error': str(e)
        }


def interface_download(video_url, noplaylist, save_path):
    """
    Gradio界面的处理函数
    """
    if not video_url:
        return "请输入视频链接！"

    # 根据选择的下载选项更新 noplaylist 参数
    noplaylist = True if noplaylist == "单个视频" else False

    if not save_path:
        save_path = config['DIR']

    # 调用下载函数
    result = download_video(video_url, noplaylist, save_path)

    if result['status'] == 'success':
        return f"✅ {result['message']}\n保存位置: {result['path']}"
    else:
        return f"❌ {result['message']}"


# 创建Gradio界面
iface = gr.Interface(
    fn=interface_download,
    inputs=[
        gr.Textbox(label="视频链接", placeholder="请输入视频链接..."),
        gr.Radio(["单个视频", "列表全部"], label="选择下载选项", value="单个视频"),
        gr.Textbox(label="保存路径", placeholder=config['DIR'], value=config['DIR'])
    ],
    outputs=gr.Textbox(label="下载状态"),
    title="视频下载器",
    description="输入视频链接和保存路径，点击提交开始下载。",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    webbrowser.open("http://localhost:7860/")
    iface.launch(share=False)
