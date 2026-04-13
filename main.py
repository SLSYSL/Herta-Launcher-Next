"""主入口文件"""

from tui import TUIApp
from module import setup_logger


def main() -> None:
    """主函数"""
    # 初始化日志记录器
    logger = setup_logger()
    logger.info("应用启动成功")

    # 运行 TUI 应用
    while True:
        # 运行 TUI 应用
        app = TUIApp()
        app.run()

        # 如果没有设置重启标志，退出程序
        if not app.restart_flag:
            break


if __name__ == "__main__":
    # 主函数
    main()
