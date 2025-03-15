import os
import yaml

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')

def load_config():
    """加载配置文件"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_key(key):
    """获取配置项"""
    config = load_config()
    keys = key.split('.')
    value = config
    for k in keys:
        value = value.get(k)
    return value