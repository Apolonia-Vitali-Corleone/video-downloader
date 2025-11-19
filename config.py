import os

# Use a dictionary to store configuration
config = {
    # 下载目录 (使用 r"" 原始字符串避免转义问题)
    'DIR': r"D:\Video",

    # 代理配置 (如果不需要代理，设置为 None 或删除此行)
    # 国内访问某些平台需要代理，国外用户可以设置为 None
    'PROXY': 'http://10.0.0.1:38964',  # 不需要代理时改为: None

    # ffmpeg 路径（存放 ffmpeg.exe, ffprobe.exe, ffplay.exe 的目录）
    "FFMPEG_PATH": os.path.join(".", "ffmpeg", "bin")
}

# 启动时自动创建下载目录
if not os.path.exists(config["DIR"]):
    os.makedirs(config["DIR"], exist_ok=True)
