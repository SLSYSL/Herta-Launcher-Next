"""日志管理器"""

import queue
from datetime import datetime
from loguru import logger
from .utils import get_install_dir

# 日志目录
LOG_DIR = get_install_dir() / "Herta-Launcher-Next-Temp" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# UI 消息队列（线程安全）
log_queue = queue.Queue()


def ui_sink(message: str) -> None:
    """UI日志处理器"""
    log_queue.put(message)


def setup_logger() -> logger:
    """配置日志记录器"""
    # 移除默认的输出处理器
    logger.remove()

    # 日志文件路径
    log_file = LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}.log"

    # 添加文件处理器
    logger.add(
        log_file,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} - "
            "{level} - "
            "{name}:{function}:{line} - "
            "{message}"
        ),
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        level="DEBUG",
        encoding="utf-8",
    )

    # 添加UI处理器
    logger.add(
        ui_sink,
        format=(
            "[green]{time:YYYY-MM-DD HH:mm:ss}[/green] - "
            "{level} - "
            "[cyan]{name}:{function}:{line}[/cyan] - "
            "{message}"
        ),
        level="INFO",
        enqueue=True,
    )

    return logger


# 导出日志记录器和队队列
__all__ = ["logger", "log_queue"]
