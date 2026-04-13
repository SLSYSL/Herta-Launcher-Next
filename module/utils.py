"""工具模块"""

import sys
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def get_install_dir() -> Path:
    """获取当前程序所在的目录"""
    # Pyinstaller
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    # 开发环境
    return Path(__file__).parent.parent.resolve()


@lru_cache(maxsize=1)
def get_runtime_dir() -> Path:
    """获取程序运行时目录"""
    # PyInstaller 单文件模式
    if hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS", None))

    # 开发环境或单目录模式
    return get_install_dir()
