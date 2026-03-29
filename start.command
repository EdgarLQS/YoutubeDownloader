#!/bin/bash
# YouTube Downloader - macOS 启动脚本
# 双击即可运行

# 获取脚本所在目录
cd "$(dirname "$0")"

# 检查是否使用 conda
if command -v conda &> /dev/null; then
    # 初始化 conda (如果尚未初始化)
    eval "$(conda shell.bash hook)"
    conda activate youtube-downloader 2>/dev/null || true
fi

# 运行程序
python3 main.py

# 如果程序退出，保持窗口打开显示消息
echo ""
echo "程序已退出。按任意键关闭此窗口..."
read -n 1
