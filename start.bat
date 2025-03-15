@echo off
chcp 65001
echo Starting YouTube Downloader...

:: Activate conda environment and run program
call conda activate youtube-downloader
python main.py
pause 