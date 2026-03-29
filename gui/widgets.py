"""
GUI 部件模块
包含自定义按钮、输入框、进度条等 UI 组件
"""
from PyQt6.QtWidgets import (
    QPushButton, QLineEdit, QProgressBar, QLabel,
    QComboBox, QFrame, QScrollArea, QWidget, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ThemedButton(QPushButton):
    """主题按钮"""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(36)


class ThemedLineEdit(QLineEdit):
    """主题输入框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)
        self.setPlaceholderText("")


class ThemedProgressBar(QProgressBar):
    """主题进度条"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(20)
        self.setValue(0)
        self.setFormat("%p%")


class ThemedLabel(QLabel):
    """主题标签"""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setWordWrap(True)


class ThemedComboBox(QComboBox):
    """主题下拉框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(36)
        self.setMinimumWidth(120)


class HistoryItemWidget(QFrame):
    """历史记录项组件"""

    remove_clicked = pyqtSignal(str)  # 发送 URL

    def __init__(self, url: str, title: str, resolution: str, downloaded_at: str, parent=None):
        super().__init__(parent)
        self.url = url
        self.setup_ui(title, resolution, downloaded_at)

    def setup_ui(self, title: str, resolution: str, downloaded_at: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        # 左侧：视频信息
        info_layout = QVBoxLayout()

        # 标题（截断过长部分）
        title_label = ThemedLabel(title[:60] + "..." if len(title) > 60 else title)
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        info_layout.addWidget(title_label)

        # 分辨率和时间
        meta_label = ThemedLabel(f"{resolution}p • {downloaded_at}")
        meta_label.setStyleSheet("color: #888; font-size: 11px;")
        info_layout.addWidget(meta_label)

        layout.addLayout(info_layout, 1)

        # 右侧：删除按钮
        delete_btn = ThemedButton("删除")
        delete_btn.setMaximumWidth(60)
        delete_btn.clicked.connect(lambda: self.remove_clicked.emit(self.url))
        layout.addWidget(delete_btn)


class HistoryListWidget(QScrollArea):
    """历史记录列表容器"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.container)

    def add_item(self, url: str, title: str, resolution: str, downloaded_at: str):
        """添加历史记录项"""
        item = HistoryItemWidget(url, title, resolution, downloaded_at)
        item.remove_clicked.connect(self._on_item_removed)
        self.layout.addWidget(item)

    def clear_items(self):
        """清空所有项"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _on_item_removed(self, url: str):
        """处理项删除"""
        self.remove_clicked.emit(url)

    remove_clicked = pyqtSignal(str)
