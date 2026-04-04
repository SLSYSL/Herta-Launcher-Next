"""Textual App"""

from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Header, TabbedContent, TabPane
from textual.containers import TabbedContent, TabPane
from .custom_widgets import BottomMenu



class TUIApp(App):
    """Textual App 主类 (Textual App main class)"""

    # 样式路径 (Application interface style path)
    CSS_PATH = "style.css"

    def __init__(self):
        """初始化应用 (Initialize the app)"""
        super().__init__()

        # 默认终端颜色 (Application default terminal color)
        self.ansi_color = True

    def compose(self) -> ComposeResult:
        """编写应用界面 (Compose the app interface)"""
        # 应用标题
        yield Header()

        # 应用标题 (Application title)
        yield Label("Herta Launcher Next", id="app-title")

        # 应用内容容器 (Application content container)
        yield Label(id="app-content-container")

        # 应用日志 (Application log)
        yield Label(id="app-log-container")

        # 底部菜单 (Bottom menu)
        with BottomMenu():
            yield Button("Select JSON", id="select_json")
            yield Button("Launch", id="launch")
            yield Button("Settings", id="settings")
            yield Button("Exit", id="exit")

    def on_mount(self) -> None:
        """应用挂载时 (Application mounted)"""
        # 初始化应用内容容器 (Application content container)
        label = self.query_one("#app-content-container")
        label.border_title = "Application Content"

        # 初始化应用日志 (Application log)
        label = self.query_one("#app-log-container")
        label.border_title = "Application Log"

    def settings(self) -> None:
        """应用设置 (Application settings)"""
        self.push_screen(SettingsPage())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件 (Handle button pressed event)"""
        if event.button.id == "exit":
            self.exit()
        elif event.button.id == "settings":
            self.settings()
