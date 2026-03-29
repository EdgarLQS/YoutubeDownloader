"""
YouTube Downloader - 跨平台 GUI 版本
支持 Windows 和 macOS
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_gui():
    """运行 GUI 界面"""
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from gui.main_window import MainWindow

    # 启用高分屏支持
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except AttributeError:
        pass  # 旧版本 PyQt6 不支持

    app = QApplication(sys.argv)
    app.setApplicationName("YouTube Downloader")
    app.setOrganizationName("YoutubeDownloader")

    # 设置应用样式
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


def run_cli():
    """运行命令行界面（保留原有功能）"""
    from core.downloader import YouTubeDownloader
    from core.config_utils import load_key

    output_dir = load_key("download.output_dir")
    default_resolution = load_key("download.ytb_resolution")

    downloader = YouTubeDownloader(output_dir=output_dir)

    while True:
        print("\n=== YouTube 视频下载器 ===")
        url = input("\n请输入 YouTube 视频链接 (输入 q 退出): ")

        if url.lower() == 'q':
            break

        print("\n可选分辨率:")
        print("1. 360p")
        print("2. 1080p")
        print("3. 最佳质量")
        choice = input("请选择分辨率 (1-3，默认为 2): ").strip()

        resolution_map = {
            "1": "360",
            "2": "1080",
            "3": "best"
        }

        resolution = resolution_map.get(choice, default_resolution)

        print(f"\n开始下载视频：{url}")
        print(f"选择的分辨率：{resolution}")

        video_file = downloader.download(url, resolution)

        if video_file:
            print(f"\n✅ 下载成功！")
            print(f"文件保存在：{video_file}")
        else:
            print("\n❌ 下载失败！")

        input("\n按回车键继续...")


if __name__ == "__main__":
    # 默认启动 GUI
    run_gui()
