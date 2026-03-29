# YouTube 视频下载器（GUI 跨平台版）

这是一个基于 PyQt6 的 YouTube 视频下载工具，支持 Windows 和 macOS。

## 系统要求

### Windows
- Windows 10/11
- Python 3.9+
- Anaconda/Miniconda（推荐）或系统 Python

### macOS
- macOS 11.0+
- Python 3.9+（系统自带或 Homebrew 安装）
- Anaconda/Miniconda（可选）

## 快速开始

### 1. 环境配置

#### 使用 Conda（推荐，完全免费）

```bash
# 安装 Miniconda（免费）
# 访问 https://docs.conda.io/projects/miniconda/en/latest/ 下载对应系统版本

# 创建虚拟环境
conda create -n youtube-downloader python=3.9 -y

# 激活环境
# Windows:
call conda activate youtube-downloader
# macOS/Linux:
conda activate youtube-downloader

# 安装依赖
pip install -r requirements.txt
```

#### 不使用 Conda（直接使用系统 Python）

```bash
# macOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 运行程序

#### macOS
```bash
# 方式 1：直接运行（需要终端）
python3 main.py

# 方式 2：双击启动（图形界面）
chmod +x start.command
./start.command
```

#### Windows
```bash
# 双击 start.bat 或命令行运行
python main.py
```

### 3. 打包成应用程序

#### macOS 打包成 .app
```bash
chmod +x build_mac.sh
./build_mac.sh
# 完成后在 dist/ 目录找到 YouTubeDownloader.app
```

#### Windows 打包成 .exe
```batch
build_win.bat
# 完成后在 dist\ 目录找到 YouTubeDownloader.exe
```

## 功能特性

- ✅ 粘贴 YouTube 链接一键下载
- ✅ 分辨率选择（360p/1080p/最佳质量）
- ✅ 实时下载进度显示
- ✅ 自定义下载目录
- ✅ 下载历史记录（可自定义存储位置）
- ✅ 主题切换（浅色/深色/跟随系统）
- ✅ 跨平台支持（Windows/macOS）

## 配置说明

配置文件位于 `config/config.yaml`：

```yaml
download:
  ytb_resolution: "1080"      # 默认分辨率
  output_dir: "downloads"     # 下载目录
  proxy: "http://127.0.0.1:7890"  # 代理地址（如需要）

history:
  enabled: true               # 启用历史记录
  storage_path: "data/history.json"  # 历史记录存储位置

ui:
  theme: "system"             # 主题：light/dark/system
  window_width: 800
  window_height: 600
```

## 下载问题排查（重要）

如果遇到 `HTTP Error 403: Forbidden` 错误：

1. **检查代理配置**
   - 在"设置"标签页中配置代理地址（如 `http://127.0.0.1:7890`）
   - 保存后重启应用

2. **代理工具配置**
   - 确保代理工具已开启全局模式
   - 检查代理工具是否支持 YouTube 视频流转发

3. **手动测试**
   ```bash
   # 测试代理是否可用
   curl -x "http://127.0.0.1:7890" https://www.youtube.com
   ```

4. **常见代理端口**
   - Clash: 7890 / 7897
   - Surge: 6152
   - Quantumult X: 8888

## 使用说明

1. **下载视频**
   - 打开应用，在"下载"标签页
   - 粘贴 YouTube 视频链接
   - 选择分辨率
   - 点击"开始下载"

2. **更改下载目录**
   - 在"下载"标签页点击"更改"按钮
   - 选择目标文件夹

3. **切换主题**
   - 切换到"设置"标签页
   - 选择浅色/深色/跟随系统

4. **查看历史**
   - 切换到"历史"标签页
   - 可查看所有下载记录
   - 支持单条删除或清空全部

## 项目结构

```
YoutubeDownloader/
├── gui/                    # GUI 模块
│   ├── __init__.py
│   ├── main_window.py      # 主窗口
│   └── widgets.py          # 自定义控件
├── core/                   # 核心逻辑
│   ├── downloader.py       # 下载器
│   ├── config_utils.py     # 配置管理
│   └── history.py          # 历史记录
├── config/                 # 配置文件
│   └── config.yaml
├── data/                   # 用户数据（下载历史等）
├── main.py                 # 程序入口
├── start.command           # macOS 启动脚本
├── start.bat               # Windows 启动脚本
├── build_mac.sh            # macOS 打包脚本
├── build_win.bat           # Windows 打包脚本
└── requirements.txt        # 依赖列表
```

## 常见问题

### Q: Conda 是免费的吗？
A: Miniconda 完全免费。Anaconda 对商业公司（员工>200）需要付费，但个人和小公司免费。

### Q: 可以使用系统 Python 吗？
A: 可以。macOS 自带 Python 3.9+，Windows 可从 python.org 安装。

### Q: 下载的视频在哪里？
A: 默认在 `downloads` 文件夹，可在界面中更改。

### Q: 历史记录可以改位置吗？
A: 可以。在"设置"标签页中更改"历史记录存储位置"。

### Q: 下载时出现 403 错误怎么办？
A: 这是 YouTube 的反爬虫限制。请在"设置"标签页配置代理地址，或在配置文件中设置 `proxy` 参数。

### Q: 打包后的应用无法打开？
A: macOS 可能会提示"无法验证开发者"。解决方法：
   - 右键点击 .app 文件，选择"打开"
   - 或在终端运行：`xattr -cr /path/to/YouTubeDownloader.app`

## 许可证

MIT License
