"""Textual App"""

from textual.app import App, SystemCommand, ComposeResult
from textual.widgets import TabbedContent, TabPane, Header, Label
from module import ConfigManager, restart_program
from .pages import HomePage, SettingsPage
from .custom_widgets import CustomFooter


class TUIApp(App):
    """Textual App 主类"""

    # 样式路径
    CSS_PATH = "style.tcss"

    # 设置标题
    TITLE = "Herta Launcher Next"

    # 按键绑定
    BINDINGS = [
        ("h", "goto_page('home')", "跳转到主页"),
        ("s", "goto_page('settings')", "跳转到设置页"),
        ("ctrl+s", "screenshot_screen", "截图当前屏幕"),
        ("ctrl+r", "restart", "重启程序"),
    ]

    def __init__(self):
        """初始化应用"""
        # 初始化父类
        super().__init__()

        # 配置管理器
        self.config = ConfigManager()

        # 默认终端颜色
        self.ansi_color = self.config.get("app.enable_ansi_color", False)

        # 默认主题
        if not self.ansi_color:
            self.theme = self.config.get("app.theme", "dracula")

    def action_help_quit(self) -> None:
        """显示退出应用提示"""
        for key, active_binding in self.active_bindings.items():
            if active_binding.binding.action in ("quit", "app.quit"):
                self.notify(f"按 [b]{key}[/b] 退出应用", title="你想要退出应用吗？")
                return

    def get_system_commands(self, screen):
        """系统命令面板"""
        # 切换主题命令 (非 ANSI 颜色模式)
        if not self.ansi_color:
            yield SystemCommand(
                title="临时切换主题",
                help="临时更改当前主题",
                callback=self.action_change_theme,
                discover=True,
            )

        # 显示帮助命令
        if screen.query("HelpPanel"):
            yield SystemCommand(
                "帮助",
                "隐藏帮助面板",
                self.action_hide_help_panel,
            )
        else:
            yield SystemCommand(
                "帮助",
                "显示帮助面板",
                self.action_show_help_panel,
            )

        # 显示最小化/最大化命令
        if screen.maximized is not None:
            yield SystemCommand(
                "最小化",
                "最小化当前窗口",
                screen.action_minimize,
            )
        elif screen.focused is not None and screen.focused.allow_maximize:
            yield SystemCommand("最大化", "最大化当前窗口", screen.action_maximize)

        # 显示截图命令
        yield SystemCommand(
            "截图",
            "保存当前页面截图",
            lambda: self.set_timer(0.1, self.deliver_screenshot),
        )

        # 显示退出应用命令
        yield SystemCommand(
            title="退出应用",
            help="关闭当前应用程序",
            callback=self.exit,
            discover=True,
        )

    def compose(self) -> ComposeResult:
        """应用界面"""
        # 应用头部
        yield Header(show_clock=True)

        # 应用内容页面
        with TabbedContent():
            with TabPane("主页", id="home"):
                yield HomePage()
            with TabPane("设置", id="settings"):
                yield SettingsPage()

        # 应用底部
        with CustomFooter():
            yield Label("H: 主页")
            yield Label("S: 设置页")
            yield Label("Ctrl+P: 命令面板")
            yield Label("Ctrl+S: 截图当前屏幕")
            yield Label("Ctrl+R: 重启程序")
            yield Label("Ctrl+Q: 退出程序")

    def action_goto_page(self, page: str) -> None:
        """跳转到指定页面"""
        self.query_one(TabbedContent).active = page

    def action_screenshot_screen(self) -> None:
        """截图当前屏幕"""
        self.set_timer(0.1, self.deliver_screenshot)

    def action_restart(self):
        """重启程序"""
        # 清理终端
        self.exit()

        # 重启程序
        restart_program()
