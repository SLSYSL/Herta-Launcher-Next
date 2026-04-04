"""Textual App"""

from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Header, Label
from .pages import HomePage, SettingsPage
from .custom_widgets import CustomFooter


class TUIApp(App):
    """Textual App 主类"""

    # 样式路径
    CSS_PATH = "style.css"

    # 设置标题
    TITLE = "Herta Launcher Next"
    SUB_TITLE = "Automation program for games"

    def __init__(self):
        """初始化应用"""
        super().__init__()

        # 默认终端颜色
        self.ansi_color = True

    def compose(self) -> ComposeResult:
        """应用界面"""
        # 应用头部
        yield Header()

        # 应用内容页面
        with TabbedContent(initial="home"):
            with TabPane("Home", id="home"):
                yield HomePage()
            with TabPane("Settings", id="settings"):
                yield SettingsPage()

        # 应用底部
        with CustomFooter():
            yield Label("Ctrl+Q: Exit")
            yield Label("Ctrl+P: Palette")
