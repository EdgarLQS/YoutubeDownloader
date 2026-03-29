import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any


class HistoryManager:
    """下载历史管理器"""

    def __init__(self, storage_path: str = 'data/history.json'):
        self.storage_path = storage_path
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """确保存储目录存在"""
        dir_path = os.path.dirname(self.storage_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_history(self) -> List[Dict[str, Any]]:
        """加载历史记录"""
        if not os.path.exists(self.storage_path):
            return []
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """保存历史记录"""
        self._ensure_storage_dir()
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def add_record(self, url: str, title: str, file_path: str, resolution: str, file_size: str = '') -> None:
        """添加下载记录"""
        history = self._load_history()
        record = {
            'url': url,
            'title': title,
            'file_path': file_path,
            'resolution': resolution,
            'file_size': file_size,
            'downloaded_at': datetime.now().isoformat(),
        }
        history.insert(0, record)  # 新记录在前
        self._save_history(history)

    def get_records(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取历史记录"""
        history = self._load_history()
        if limit:
            return history[:limit]
        return history

    def clear(self) -> None:
        """清空历史记录"""
        self._save_history([])

    def remove_record(self, url: str) -> bool:
        """删除指定记录"""
        history = self._load_history()
        original_len = len(history)
        history = [r for r in history if r['url'] != url]
        if len(history) < original_len:
            self._save_history(history)
            return True
        return False

    def update_storage_path(self, new_path: str) -> None:
        """更新存储路径并迁移数据"""
        old_path = self.storage_path
        if os.path.exists(old_path):
            self._ensure_storage_dir()
            with open(old_path, 'r', encoding='utf-8') as f:
                data = f.read()
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(data)
            os.remove(old_path)
        self.storage_path = new_path
