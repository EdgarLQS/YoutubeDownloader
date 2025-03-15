# YouTube 视频下载器

这是一个基于 yt-dlp 的 YouTube 视频下载工具。

## 系统要求

- Windows 操作系统
- [Anaconda](https://www.anaconda.com/download) 或 [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)

## 环境配置（首次使用必读）

打开命令提示符（CMD）或 PowerShell，依次执行以下命令：

```bash
# 创建虚拟环境
conda create -n youtube-downloader python=3.9
## 删除虚拟环境 conda env remove -n youtube-downloader

# 激活虚拟环境
conda activate youtube-downloader

# 安装依赖包
pip install yt-dlp>=2023.12.30 pyyaml>=6.0.1
```

## 使用说明

1. 完成环境配置后，直接双击运行 `start.bat` 即可启动程序
2. 如需更新依赖包，请运行：
   ```bash
   conda activate youtube-downloader
   pip install -U yt-dlp pyyaml
   ```

## 配置说明

配置文件位于 `config/config.yaml`，可以根据需要修改下载参数：

```yaml
# 示例配置
download:
  output_dir: "downloads"  # 下载目录
  format: "bestvideo+bestaudio/best"  # 下载格式
```

## 注意事项

- 请确保您的网络连接稳定
- 下载视频前请确认您拥有相应的权限
- 建议使用代理以获得更好的下载体验

## 许可证

本项目基于 MIT 许可证开源。
