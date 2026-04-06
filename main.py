"""主入口文件"""

import os
from tui.app import TUIApp
from module.logger_manager import setup_logger


def main():
    """主函数"""
    # 设置终端标题
    os.system(f"title {TUIApp.TITLE}")

    # 初始化日志记录器
    logger = setup_logger()
    logger.info("应用启动成功")

    # 运行 TUI 应用
    TUIApp().run()

    # 记录应用退出日志
    logger.info("应用退出成功")


if __name__ == "__main__":
    main()
