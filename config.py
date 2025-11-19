import os

# Use a dictionary to store configuration
config = {
    'DIR': "D:\Video",
    'PROXY': 'http://10.0.0.1:38964',
    # ffmpeg 路径（适配你之前想放在同级目录的需求）
    "FFMPEG_PATH": os.path.join(".", "ffmpeg", "bin")
}

if not os.path.exists(config["DIR"]):
    os.makedirs(config["DIR"], exist_ok=True)
