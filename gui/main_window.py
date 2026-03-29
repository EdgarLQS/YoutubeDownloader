"""
主窗口模块
YouTube Downloader 的主界面
"""
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QFileDialog, QMessageBox, QFrame,
    QLabel, QGroupBox, QRadioButton, QButtonGroup, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QStandardPaths
from PyQt6.QtGui import QFont

from .widgets import (
    ThemedButton, ThemedLineEdit, ThemedProgressBar,
    ThemedLabel, ThemedComboBox, HistoryListWidget
)
from core.downloader import YouTubeDownloader
from core.config_utils import load_key, save_key, get_theme_colors
from core.history import HistoryManager


class DownloadWorker(QThread):
    """下载工作线程"""
    progress = pyqtSignal(dict)
    finished = pyqtSignal(dict)

    def __init__(self, downloader: YouTubeDownloader, url: str, resolution: str):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.resolution = resolution

    def run(self):
        result = self.downloader.download(self.url, self.resolution)
        if result:
            self.finished.emit(result)
        else:
            self.finished.emit({'success': False, 'error': '下载失败'})


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.history_manager = HistoryManager()
        self.current_theme = 'light'
        self.setup_ui()
        self.apply_theme()
        self.load_history()

    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("YouTube Downloader")
        self.setMinimumSize(800, 600)

        # 中心部件
        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        main_layout = QVBoxLayout(center_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标签页
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, 1)

        # 下载标签页
        download_tab = self.create_download_tab()
        self.tabs.addTab(download_tab, "下载")

        # 设置标签页
        settings_tab = self.create_settings_tab()
        self.tabs.addTab(settings_tab, "设置")

        # 历史标签页
        history_tab = self.create_history_tab()
        self.tabs.addTab(history_tab, "历史")

    def create_download_tab(self) -> QWidget:
        """创建下载标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        # URL 输入
        url_group = QGroupBox("视频链接")
        url_layout = QHBoxLayout(url_group)
        self.url_input = ThemedLineEdit()
        self.url_input.setPlaceholderText("粘贴 YouTube 视频链接...")
        url_layout.addWidget(self.url_input)

        download_btn = ThemedButton("开始下载")
        download_btn.clicked.connect(self.start_download)
        url_layout.addWidget(download_btn)

        layout.addWidget(url_group)

        # 分辨率选择
        res_group = QGroupBox("分辨率")
        res_layout = QHBoxLayout(res_group)
        self.resolution_group = QButtonGroup()

        for i, (value, text) in enumerate([("360", "360p"), ("1080", "1080p"), ("best", "最佳质量")]):
            radio = QRadioButton(text)
            radio.setProperty("resolution", value)
            self.resolution_group.addButton(radio)
            res_layout.addWidget(radio)
            if value == load_key("download.ytb_resolution", "1080"):
                radio.setChecked(True)

        layout.addWidget(res_group)

        # 进度显示
        progress_group = QGroupBox("下载进度")
        progress_layout = QVBoxLayout(progress_group)

        self.status_label = ThemedLabel("就绪")
        progress_layout.addWidget(self.status_label)

        self.progress_bar = ThemedProgressBar()
        progress_layout.addWidget(self.progress_bar)

        layout.addWidget(progress_group)

        # 下载目录
        dir_group = QGroupBox("下载目录")
        dir_layout = QHBoxLayout(dir_group)

        self.dir_label = ThemedLabel(load_key("download.output_dir", "downloads"))
        dir_layout.addWidget(self.dir_label, 1)

        change_dir_btn = ThemedButton("更改")
        change_dir_btn.clicked.connect(self.change_download_dir)
        dir_layout.addWidget(change_dir_btn)

        open_dir_btn = ThemedButton("打开目录")
        open_dir_btn.clicked.connect(self.open_download_dir)
        dir_layout.addWidget(open_dir_btn)

        layout.addWidget(dir_group)

        layout.addStretch()
        return widget

    def create_settings_tab(self) -> QWidget:
        """创建设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        # 代理设置
        proxy_group = QGroupBox("代理设置（如需要）")
        proxy_layout = QHBoxLayout(proxy_group)

        proxy_layout.addWidget(ThemedLabel("代理地址:"))
        self.proxy_input = ThemedLineEdit()
        self.proxy_input.setPlaceholderText("例如：http://127.0.0.1:7890")
        self.proxy_input.setText(load_key("download.proxy", ""))
        proxy_layout.addWidget(self.proxy_input)

        save_proxy_btn = ThemedButton("保存")
        save_proxy_btn.clicked.connect(self.save_proxy)
        proxy_layout.addWidget(save_proxy_btn)

        layout.addWidget(proxy_group)

        # 主题设置
        theme_group = QGroupBox("界面主题")
        theme_layout = QHBoxLayout(theme_group)

        self.theme_group = QButtonGroup()
        for value, text in [("light", "浅色"), ("dark", "深色"), ("system", "跟随系统")]:
            radio = QRadioButton(text)
            radio.setProperty("theme", value)
            self.theme_group.addButton(radio)
            theme_layout.addWidget(radio)
            if value == load_key("ui.theme", "system"):
                radio.setChecked(True)

        self.theme_group.buttonClicked.connect(self.change_theme)
        layout.addWidget(theme_group)

        # 历史记录路径
        history_group = QGroupBox("历史记录存储位置")
        history_layout = QHBoxLayout(history_group)

        self.history_path_label = ThemedLabel(load_key("history.storage_path", "data/history.json"))
        history_layout.addWidget(self.history_path_label, 1)

        change_history_btn = ThemedButton("更改")
        change_history_btn.clicked.connect(self.change_history_path)
        history_layout.addWidget(change_history_btn)

        layout.addWidget(history_group)

        layout.addStretch()
        return widget

    def create_history_tab(self) -> QWidget:
        """创建历史标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 工具栏
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addStretch()

        clear_btn = ThemedButton("清空历史")
        clear_btn.clicked.connect(self.clear_history)
        toolbar_layout.addWidget(clear_btn)

        layout.addLayout(toolbar_layout)

        # 历史列表
        self.history_list = HistoryListWidget()
        self.history_list.remove_clicked.connect(self.remove_history_item)
        layout.addWidget(self.history_list)

        return widget

    def start_download(self):
        """开始下载"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "警告", "请输入视频链接")
            return

        # 获取选中的分辨率
        resolution = "1080"
        for btn in self.resolution_group.buttons():
            if btn.isChecked():
                resolution = btn.property("resolution")
                break

        # 保存设置
        save_key("download.ytb_resolution", resolution)

        # 创建下载器（带代理配置）
        output_dir = load_key("download.output_dir", "downloads")
        proxy = load_key("download.proxy", "")
        downloader = YouTubeDownloader(output_dir=output_dir, progress_callback=self.on_progress, proxy=proxy)

        # 启动下载线程
        self.status_label.setText("正在下载...")
        self.progress_bar.setValue(0)
        self.download_btn_backup = None  # 用于恢复按钮状态

        self.worker = DownloadWorker(downloader, url, resolution)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.start()

    def on_progress(self, data: dict):
        """进度更新"""
        if 'status' in data:
            if data['status'] == 'downloading':
                total = data.get('total_bytes') or data.get('total_bytes_estimate', 0)
                downloaded = data.get('downloaded_bytes', 0)
                if total > 0:
                    percent = int(downloaded / total * 100)
                    self.progress_bar.setValue(percent)
                    speed = data.get('speed')
                    if speed:
                        if isinstance(speed, (int, float)):
                            speed = f"{speed:.2f} B/s"
                        elif isinstance(speed, bytes):
                            speed = speed.decode('utf-8', errors='ignore')
                    else:
                        speed = ''
                    self.status_label.setText(f"下载中... {percent}% ({speed})")
            elif data['status'] == 'finished':
                self.progress_bar.setValue(100)
                self.status_label.setText("下载完成，处理中...")

    def on_download_finished(self, result: dict):
        """下载完成"""
        if result.get('success'):
            self.status_label.setText(f"✅ 下载完成：{result.get('title', '')}")
            self.progress_bar.setValue(100)
            self.url_input.clear()

            # 添加到历史
            self.history_manager.add_record(
                url=self.url_input.text() if hasattr(self, 'url_input') else '',
                title=result.get('title', ''),
                file_path=result.get('file_path', ''),
                resolution=result.get('resolution', ''),
                file_size=result.get('file_size', '')
            )

            # 刷新历史列表
            self.load_history()

            QMessageBox.information(self, "成功", f"视频已下载到:\n{result.get('file_path', '')}")
        else:
            self.status_label.setText("下载失败")
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, "错误", f"下载失败：{result.get('error', '未知错误')}")

    def change_download_dir(self):
        """更改下载目录"""
        current = load_key("download.output_dir", "downloads")
        if not os.path.isabs(current):
            current = os.path.join(os.getcwd(), current)

        directory = QFileDialog.getExistingDirectory(
            self, "选择下载目录", current,
            QFileDialog.Option.ShowDirsOnly
        )
        if directory:
            save_key("download.output_dir", directory)
            self.dir_label.setText(directory)

    def open_download_dir(self):
        """打开下载目录"""
        output_dir = load_key("download.output_dir", "downloads")
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(os.getcwd(), output_dir)

        if os.path.exists(output_dir):
            # 跨平台打开目录
            import subprocess
            if os.name == 'nt':
                os.startfile(output_dir)
            elif os.name == 'posix':
                subprocess.run(['open', output_dir])  # macOS
            else:
                subprocess.run(['xdg-open', output_dir])  # Linux

    def change_theme(self, button: QRadioButton):
        """更改主题"""
        theme = button.property("theme")
        save_key("ui.theme", theme)

        # 如果是跟随系统，需要检测系统主题
        if theme == 'system':
            # macOS 和 Windows 都有方式检测系统主题
            # 这里简化处理，默认浅色
            theme = 'light'

        self.current_theme = theme
        self.apply_theme()

    def apply_theme(self):
        """应用主题"""
        colors = get_theme_colors(self.current_theme)

        # 构建样式表
        stylesheet = f"""
        QMainWindow, QWidget {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
        }}
        QGroupBox {{
            font-weight: bold;
            border: 1px solid {colors['border']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
            color: {colors['accent']};
        }}
        QLineEdit {{
            background-color: {colors['bg_secondary']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            color: {colors['text_primary']};
        }}
        QLineEdit:focus {{
            border-color: {colors['accent']};
        }}
        QPushButton {{
            background-color: {colors['accent']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            opacity: 0.9;
        }}
        QPushButton:pressed {{
            opacity: 0.8;
        }}
        QProgressBar {{
            background-color: {colors['bg_secondary']};
            border: 1px solid {colors['border']};
            border-radius: 10px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: {colors['accent']};
            border-radius: 10px;
        }}
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            border-radius: 8px;
        }}
        QTabBar::tab {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_secondary']};
            padding: 10px 20px;
            border: 1px solid {colors['border']};
            border-radius: 6px;
            margin-right: 4px;
        }}
        QTabBar::tab:selected {{
            background-color: {colors['bg_primary']};
            color: {colors['accent']};
        }}
        QRadioButton {{
            color: {colors['text_primary']};
        }}
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
        }}
        QRadioButton::indicator:checked {{
            background-color: {colors['accent']};
            border: 2px solid {colors['border']};
            border-radius: 9px;
        }}
        QScrollArea {{
            border: 1px solid {colors['border']};
            border-radius: 6px;
            background-color: {colors['bg_secondary']};
        }}
        """

        self.setStyleSheet(stylesheet)

    def change_history_path(self):
        """更改历史记录存储路径"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "选择历史记录存储位置",
            load_key("history.storage_path", "data/history.json"),
            "JSON Files (*.json)"
        )
        if file_path:
            self.history_manager.update_storage_path(file_path)
            save_key("history.storage_path", file_path)
            self.history_path_label.setText(file_path)

    def load_history(self):
        """加载历史记录"""
        self.history_list.clear_items()
        records = self.history_manager.get_records(limit=50)
        for record in records:
            downloaded_at = record.get('downloaded_at', '')[:10]  # 只显示日期
            self.history_list.add_item(
                url=record.get('url', ''),
                title=record.get('title', ''),
                resolution=record.get('resolution', ''),
                downloaded_at=downloaded_at
            )

    def clear_history(self):
        """清空历史"""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有下载历史吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.history_manager.clear()
            self.load_history()

    def remove_history_item(self, url: str):
        """删除历史记录"""
        self.history_manager.remove_record(url)
        self.load_history()

    def save_proxy(self):
        """保存代理配置"""
        proxy = self.proxy_input.text().strip()
        save_key("download.proxy", proxy)
        if proxy:
            QMessageBox.information(self, "代理设置", f"代理已保存：{proxy}\n请重启应用后生效")
        else:
            QMessageBox.information(self, "代理设置", "已清空代理配置，将直连 YouTube")

