import os
import sys
import yt_dlp
import subprocess
from typing import Optional, Callable, Dict, Any
import re


class YouTubeDownloader:
    def __init__(self, output_dir: str = "downloads", progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None, proxy: str = ""):
        self.output_dir = output_dir
        self.progress_callback = progress_callback
        self.proxy = proxy
        os.makedirs(output_dir, exist_ok=True)
        self._update_yt_dlp()

    def _update_yt_dlp(self):
        """更新 yt-dlp 到最新版本"""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        except subprocess.CalledProcessError as e:
            print(f"警告：更新 yt-dlp 失败：{e}")

    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.strip('. ')
        return filename if filename else 'video'

    def _progress_hook(self, d: Dict[str, Any]) -> None:
        """进度回调钩子"""
        if self.progress_callback:
            self.progress_callback(d)

    def download(self, url: str, resolution: str = "1080") -> Optional[Dict[str, Any]]:
        """
        下载 YouTube 视频

        参数:
            url: YouTube 视频链接
            resolution: 视频分辨率 ("360", "1080", "best")

        返回:
            dict: 包含下载结果信息，如果下载失败则返回 None
                - success: bool
                - file_path: str (下载的文件路径)
                - title: str (视频标题)
                - resolution: str (实际分辨率)
                - file_size: str (文件大小)
        """
        allowed_resolutions = ['360', '1080', 'best']
        if resolution not in allowed_resolutions:
            resolution = '1080'

        download_result = {
            'success': False,
            'file_path': None,
            'title': '',
            'resolution': resolution,
            'file_size': '',
        }

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if resolution == 'best' else f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self._progress_hook],
            # 绕过 YouTube 限制的参数
            # 使用 android_vr 客户端绕过 YouTube 的 IP 绑定验证和 GVS PO Token 要求
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_vr'],
                }
            },
            # 自动继承系统代理环境变量
            'http_proxy': os.environ.get('http_proxy') or os.environ.get('HTTP_PROXY'),
            'https_proxy': os.environ.get('https_proxy') or os.environ.get('HTTPS_PROXY'),
            'no_proxy': os.environ.get('no_proxy') or os.environ.get('NO_PROXY'),
        }

        # 手动配置代理（优先级高于环境变量）
        if self.proxy:
            ydl_opts['proxy'] = self.proxy

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                filename = ydl.prepare_filename(info)
                clean_filename = self._sanitize_filename(os.path.basename(filename))
                final_path = os.path.join(self.output_dir, clean_filename)

                if os.path.exists(filename) and filename != final_path:
                    os.rename(filename, final_path)

                # 获取文件大小
                file_size = ''
                if os.path.exists(final_path):
                    size_bytes = os.path.getsize(final_path)
                    if size_bytes > 1024 * 1024 * 1024:
                        file_size = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
                    elif size_bytes > 1024 * 1024:
                        file_size = f"{size_bytes / (1024 * 1024):.2f} MB"
                    elif size_bytes > 1024:
                        file_size = f"{size_bytes / 1024:.2f} KB"
                    else:
                        file_size = f"{size_bytes} B"

                download_result.update({
                    'success': True,
                    'file_path': final_path,
                    'title': title,
                    'file_size': file_size,
                })
                return download_result

        except Exception as e:
            print(f"下载失败：{e}")
            download_result['error'] = str(e)
            return None
