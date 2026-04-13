"""自定义组件"""

from textual.containers import Horizontal
from textual.widgets import MarkdownViewer


class CustomMarkdownViewer(MarkdownViewer):
    """自定义 Markdown 查看器，拦截外部链接"""
    async def go(self, location: str) -> None:
        """拦截 go 方法，处理外部链接"""
        if location.startswith(("http://", "https://")):
            # 不调用父类，直接返回，避免文件路径错误
            return
        # 内部锚点或本地路径，交给父类处理
        await super().go(location)


class CustomFooter(Horizontal):
    """自定义应用底部组件"""

    DEFAULT_CSS = """
    CustomFooter {
        dock: bottom;
        layout: grid;
        grid-size: 3 2;
        height: auto;
        align: center middle;
    }
    CustomFooter Label {
        margin: 0 4;
        color: #454545;
    }
    """
