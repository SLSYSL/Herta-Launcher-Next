"""工具模块"""

import sys
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def get_install_dir() -> Path:
    """获取当前程序所在的目录（开发环境脚本目录 / 生产环境 exe 目录）"""
    # 检查是否为打包后的 exe 环境
    if getattr(sys, "frozen", False):
        # 打包后的 exe 环境
        base_dir = Path(sys.executable).parent
    else:
        # 开发环境：获取脚本所在目录
        base_dir = Path(__file__).parent.parent
    return base_dir


@lru_cache(maxsize=1)
def get_runtime_dir() -> Path:
    """获取程序运行时目录 (PyInstaller 解压的 _MEIxxxxx 临时文件夹)"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller 单文件模式：返回临时解压目录 _MEIxxxxx
        return Path(getattr(sys, "_MEIPASS", None))
    else:
        # 开发环境或单目录模式
        return Path(__file__).parent.parent.resolve()
