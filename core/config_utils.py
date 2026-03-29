import os
import yaml
from typing import Any, Optional

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')

DEFAULT_CONFIG = {
    'download': {
        'ytb_resolution': '1080',
        'output_dir': 'downloads',
    },
    'history': {
        'enabled': True,
        'storage_path': 'data/history.json',
    },
    'ui': {
        'theme': 'system',  # 'light', 'dark', 'system'
        'window_width': 800,
        'window_height': 600,
    }
}


def load_config() -> dict:
    """加载配置文件，如果不存在则创建默认配置"""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(DEFAULT_CONFIG, f, allow_unicode=True, default_flow_style=False)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 合并默认配置（确保新添加的配置项存在）
    merged = DEFAULT_CONFIG.copy()
    if config:
        for key, value in config.items():
            if isinstance(value, dict) and key in merged:
                merged[key].update(value)
            else:
                merged[key] = value
    return merged


def save_config(config: dict) -> None:
    """保存配置文件"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def load_key(key: str, default: Any = None) -> Any:
    """获取配置项"""
    config = load_config()
    keys = key.split('.')
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default
    return value if value is not None else default


def save_key(key: str, value: Any) -> None:
    """保存配置项"""
    config = load_config()
    keys = key.split('.')
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]
    current[keys[-1]] = value
    save_config(config)


def get_theme_colors(theme: str) -> dict:
    """获取主题颜色配置"""
    themes = {
        'light': {
            'bg_primary': '#ffffff',
            'bg_secondary': '#f5f5f5',
            'text_primary': '#000000',
            'text_secondary': '#666666',
            'accent': '#007AFF',
            'border': '#e0e0e0',
            'success': '#34C759',
            'error': '#FF3B30',
        },
        'dark': {
            'bg_primary': '#1c1c1e',
            'bg_secondary': '#2c2c2e',
            'text_primary': '#ffffff',
            'text_secondary': '#98989d',
            'accent': '#0A84FF',
            'border': '#3a3a3c',
            'success': '#30D158',
            'error': '#FF453A',
        }
    }
    return themes.get(theme, themes['light'])
