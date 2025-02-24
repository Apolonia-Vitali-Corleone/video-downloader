import gradio as gr
from function import download_video
import webbrowser
import constant


def download_interface(video_url, save_path):
    """
    Gradio界面的处理函数
    """
    if not save_path:
        save_path = constant.Constant.DIR

    if not video_url:
        return "请输入视频链接！"

    # 调用下载函数
    result = download_video(video_url, save_path)

    if result['status'] == 'success':
        return f"✅ {result['message']}\n保存位置: {result['path']}"
    else:
        return f"❌ {result['message']}"


# 创建Gradio界面
iface = gr.Interface(
    fn=download_interface,
    inputs=[
        gr.Textbox(label="视频链接", placeholder="请输入视频链接..."),
        gr.Textbox(label="保存路径", placeholder=constant.Constant.DIR, value=constant.Constant.DIR)
    ],
    outputs=gr.Textbox(label="下载状态"),
    title="视频下载器",
    description="输入视频链接和保存路径，点击提交开始下载。",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    webbrowser.open("http://localhost:7860/")
    iface.launch(share=False)
