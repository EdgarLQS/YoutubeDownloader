import os
import sys
from core.downloader import YouTubeDownloader
from core.config_utils import load_key

def main():
    # 从配置文件加载设置
    output_dir = load_key("download.output_dir")
    default_resolution = load_key("download.ytb_resolution")
    
    # 创建下载器实例
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
        choice = input("请选择分辨率 (1-3，默认为2): ").strip()
        
        resolution_map = {
            "1": "360",
            "2": "1080",
            "3": "best"
        }
        
        resolution = resolution_map.get(choice, default_resolution)
        
        # 开始下载
        print(f"\n开始下载视频: {url}")
        print(f"选择的分辨率: {resolution}")
        
        video_file = downloader.download(url, resolution)
        
        if video_file:
            print(f"\n✅ 下载成功！")
            print(f"文件保存在: {video_file}")
        else:
            print("\n❌ 下载失败！")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已退出程序")
    except Exception as e:
        print(f"\n程序出错: {e}")