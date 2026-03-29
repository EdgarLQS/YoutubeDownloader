@echo off
chcp 65001
echo === YouTube Downloader - Windows 打包 ===

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：需要安装 Python
    pause
    exit /b 1
)

REM 安装打包工具
echo 安装 PyInstaller...
pip install pyinstaller pyqt6 yt-dlp pyyaml

REM 清理旧的构建文件
echo 清理旧的构建文件...
rmdir /s /q build dist 2>nul
del /q *.spec 2>nul

REM 运行 PyInstaller
echo 开始打包...
pyinstaller build.spec

echo.
echo === 打包完成 ===
echo 应用程序位于：dist\YouTubeDownloader.exe
echo.
pause
