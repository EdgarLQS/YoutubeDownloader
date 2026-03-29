# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube video downloader with PyQt6 GUI. Supports Windows and macOS. Downloads videos using yt-dlp with proxy support to bypass regional restrictions.

## Common Commands

```bash
# Run application
python3 main.py

# Install dependencies
pip install -r requirements.txt

# Package for macOS (.app)
./build_mac.sh

# Package for Windows (.exe)
build_win.bat
```

## Architecture

```
YoutubeDownloader/
├── main.py              # Entry point (GUI/CLI)
├── gui/
│   ├── main_window.py   # Main window, tabs (Download/Settings/History)
│   └── widgets.py       # Custom themed widgets
├── core/
│   ├── downloader.py    # yt-dlp wrapper, handles video download
│   ├── config_utils.py  # YAML config load/save utilities
│   └── history.py       # Download history (JSON storage)
├── config/
│   └── config.yaml      # User configuration
└── data/                # User data (history.json)
```

## Key Components

**`core/downloader.py`** - `YouTubeDownloader` class
- Uses `android_vr` player client to bypass YouTube's IP binding and GVS PO Token requirements
- Downloads run in background thread (`DownloadWorker` in main_window.py)
- Progress callbacks via `_progress_hook()`

**`gui/main_window.py`** - `MainWindow` class
- 3 tabs: Download, Settings, History
- `start_download()` creates downloader and starts worker thread
- `on_progress()` handles speed data that may be float or bytes

**`core/config_utils.py`** - Configuration management
- `load_key()` / `save_key()` for nested YAML access
- Theme colors: light/dark/system

## Important Notes

**YouTube Download Fix (2026):**
- Uses `player_client: ['android_vr']` instead of `['ios', 'web']`
- ios/web clients require GVS PO Token and fail with HTTP 403
- android_vr bypasses IP binding validation

**Proxy Configuration:**
- Configured in `config/config.yaml` or Settings tab
- Required for users in regions with YouTube restrictions
- Format: `http://127.0.0.1:7897`

**Speed Handling:**
- yt-dlp progress callback may return speed as float or bytes
- Always check type before decoding: `isinstance(speed, (int, float))`
