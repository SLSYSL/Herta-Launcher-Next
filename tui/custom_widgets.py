"""自定义组件"""

from textual.containers import Horizontal, Vertical
from textual.widgets import Label


class CustomFooter(Horizontal):
    """自定义应用底部"""

    DEFAULT_CSS = """
    CustomFooter {
        dock: bottom;
        height: 3;
        align: center middle;
    }
    CustomFooter Label {
        margin: 0 2;
        color: #454545;
    }
    """
