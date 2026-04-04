"""页面模块"""

from textual.containers import Container, VerticalScroll
from textual.widgets import Label


class HomePage(Container):
    """首页页面"""

    def compose(self):
        """编写首页界面"""
        with VerticalScroll(id="app-content-container", classes="app-container"):
            yield Label("Application Content")
        yield Label(id="app-log-container", classes="app-container")

    def on_mount(self) -> None:
        """应用挂载时 (Application mounted)"""
        # 初始化应用内容容器
        label = self.query_one("#app-content-container")
        label.border_title = "Application Content"

        # 初始化应用日志
        label = self.query_one("#app-log-container")
        label.border_title = "Application Log"


class SettingsPage(Container):
    """设置页面"""

    def compose(self):
        """编写设置界面"""
        yield Label("Settings Page")
