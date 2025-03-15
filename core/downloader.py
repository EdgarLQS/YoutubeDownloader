import os
import sys
import yt_dlp
import subprocess
from typing import Optional
import re

class YouTubeDownloader:
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._update_yt_dlp()

    def _update_yt_dlp(self):
        """更新 yt-dlp 到最新版本"""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        except subprocess.CalledProcessError as e:
            print(f"警告: 更新 yt-dlp 失败: {e}")

    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.strip('. ')
        return filename if filename else 'video'

    def download(self, url: str, resolution: str = "1080") -> Optional[str]:
        """
        下载 YouTube 视频
        
        参数:
            url: YouTube 视频链接
            resolution: 视频分辨率 ("360", "1080", "best")
            
        返回:
            str: 下载的视频文件路径，如果下载失败则返回 None
        """
        allowed_resolutions = ['360', '1080', 'best']
        if resolution not in allowed_resolutions:
            resolution = '1080'

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if resolution == 'best' else f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'progress': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                clean_filename = self._sanitize_filename(os.path.basename(filename))
                final_path = os.path.join(self.output_dir, clean_filename)
                
                if os.path.exists(filename) and filename != final_path:
                    os.rename(filename, final_path)
                
                return final_path
        except Exception as e:
            print(f"下载失败: {e}")
            return None