@echo off
chcp 65001
echo Starting YouTube Downloader GUI...

:: Activate conda environment and run program
call conda activate youtube-downloader 2>nul
if errorlevel 1 (
    echo Conda environment not found, using system Python...
)

python main.py
pause
