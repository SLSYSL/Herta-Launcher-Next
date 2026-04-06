"""自定义组件"""

from textual.containers import Horizontal


class CustomFooter(Horizontal):
    """自定义应用底部组件"""

    DEFAULT_CSS = """
    CustomFooter {
        dock: bottom;
        layout: grid;
        grid-size: 4;
        height: auto;
        align: center middle;
    }
    CustomFooter Label {
        margin: 0 4;
        color: #454545;
    }
    """
