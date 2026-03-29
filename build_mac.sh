#!/bin/bash
# macOS 打包脚本
# 生成 .app 应用程序

set -e

echo "=== YouTube Downloader - macOS 打包 ==="

# 检查依赖
if ! command -v pip3 &> /dev/null; then
    echo "错误：需要安装 pip3"
    exit 1
fi

# 安装打包工具
echo "安装 PyInstaller..."
pip3 install pyinstaller pyqt6 yt-dlp pyyaml

# 清理旧的构建文件
echo "清理旧的构建文件..."
rm -rf build dist __pycache__ gui/__pycache__ core/__pycache__

# 创建 icon 文件（如果没有）
if [ ! -f "icon.icns" ]; then
    echo "警告：未找到 icon.icns，将使用默认图标"
fi

# 运行 PyInstaller（使用完整路径）
echo "开始打包..."
python3 -m PyInstaller "$@" build.spec

echo ""
echo "=== 打包完成 ==="
echo "应用程序位于：dist/YouTubeDownloader.app"
echo ""
echo "可以将 .app 文件拖入 /Applications 文件夹安装"
