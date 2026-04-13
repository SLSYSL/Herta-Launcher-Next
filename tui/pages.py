"""页面模块"""

import queue
from textual import on
from textual.containers import ScrollableContainer, VerticalScroll, Horizontal
from textual.widgets import Label, RichLog, Checkbox, Select
from module import log_queue, get_runtime_dir
from .custom_widgets import CustomMarkdownViewer


class HomePage(ScrollableContainer):
    """首页页面"""

    def __init__(self):
        """初始化首页页面"""
        super().__init__()
        self.log_timer = None

    def compose(self):
        """编写首页界面"""
        # 应用内容容器
        with VerticalScroll(
            id="app-content-container", classes="app-container"
        ) as container:
            # 设置边框标题
            container.border_title = "应用公告"

            # 页面内容
            try:
                with open(
                    get_runtime_dir() / "assets" / "announcement.md",
                    "r",
                    encoding="utf-8",
                ) as f:
                    content = f.read()
                yield CustomMarkdownViewer(content)
            except FileNotFoundError:
                yield Label("应用公告文件不存在")

        # 应用日志容器
        with VerticalScroll(
            id="app-log-container", classes="app-container"
        ) as container:
            # 设置边框标题
            container.border_title = "应用日志"

            # 页面内容
            yield RichLog(id="app-log", markup=True, wrap=True)

    def on_mount(self) -> None:
        """应用挂载时"""
        # 初始化日志队列定时器，每0.1秒检查一次队列
        self.log_timer = self.set_interval(0.1, self.pull_logs)

    def pull_logs(self):
        """从队列中取出所有待显示的日志，并写入 RichLog"""
        logs = []
        # 从队列中取出所有待显示的日志
        while not log_queue.empty():
            try:
                msg = log_queue.get_nowait()
                logs.append(msg.strip())
            except queue.Empty:
                break

        # 写入日志到 RichLog
        if logs:
            rich_log = self.query_one("#app-log")
            for log_line in logs:
                rich_log.write(log_line)


class SettingsPage(ScrollableContainer):
    """设置页面"""

    def __init__(self):
        """初始化设置页面"""
        super().__init__()

    def compose(self):
        """编写设置界面"""
        with VerticalScroll(
            id="settings-container", classes="app-container"
        ) as container:
            # 设置边框标题
            container.border_title = "设置"

            # 常规设置
            yield Label("常规设置:", classes="setting-title")
            with Horizontal():
                yield Checkbox(
                    "启用终端默认颜色",
                    id="ansi-color-checkbox",
                    value=self.app.config.get("app.enable_ansi_color", False),
                )

            # 主题设置
            if not self.app.ansi_color:
                yield Label("主题设置:", classes="setting-title")
                yield Select[str](
                    [(theme, theme) for theme in self.app.available_themes],
                    prompt="注意此项设置仅在非“终端默认颜色”模式下生效",
                    value=self.app.theme,
                    id="theme-select",
                )

    @on(Checkbox.Changed, "#ansi-color-checkbox")
    def on_ansi_color_checkbox(self, event: Checkbox.Changed) -> None:
        """处理终端默认颜色复选框变化"""
        self.app.config.set("app.enable_ansi_color", event.value)
        self.notify("重启应用以生效")

    @on(Select.Changed, "#theme-select")
    def on_theme_select(self, event: Select.Changed) -> None:
        """处理主题选择变化"""
        # 防抖处理
        current_theme = self.app.config.get("app.theme")
        if current_theme == event.value:
            return

        # 更新应用主题
        setattr(self.app, "theme", event.value)
        self.app.config.set("app.theme", event.value)
        self.notify(f"主题已设置为: {event.value}")
