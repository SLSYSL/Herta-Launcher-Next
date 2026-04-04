"""主入口文件"""

import os
from tui.app import TUIApp


def main():
    """主函数"""
    # 设置终端标题
    os.system(f"title {TUIApp.TITLE}")

    # 运行 TUI 应用
    TUIApp().run()


if __name__ == "__main__":
    main()
