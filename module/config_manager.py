"""配置管理器"""

from typing import Any, Dict
import orjson
from loguru import logger
from module.utils import get_install_dir


class ConfigManager:
    """配置管理器"""

    # 默认配置
    DEFAULT_CONFIG: Dict[str, Any] = {
        "app": {
            "enable_ansi_color": False,
            "theme": "dracula",
        },
    }

    def __init__(self):
        """初始化配置管理器
        Args:
            config_path (Path, optional): 配置文件路径
        """
        self.config_path = get_install_dir() / "Herta-Launcher-Next-Temp" / "config.json"
        self._config: Dict[str, Any] = {}
        self.load()

    def _merge_defaults(self) -> None:
        """递归合并默认配置，确保缺失的键被补全"""

        # 递归合并默认配置
        def merge(base: dict, default: dict):
            for key, value in default.items():
                if key not in base:
                    base[key] = value
                elif isinstance(value, dict) and isinstance(base.get(key), dict):
                    merge(base[key], value)

        # 合并默认配置
        merge(self._config, self.DEFAULT_CONFIG)

    def load(self) -> None:
        """从文件加载配置，如果文件不存在则创建默认配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, "rb") as f:
                    self._config = orjson.loads(f.read())
                # 合并默认配置，确保新增的默认字段存在
                self._merge_defaults()
            except (orjson.JSONDecodeError, OSError, IOError) as e:
                logger.error("加载配置失败: {}，使用默认配置", e)
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
            self.save()

    def save(self) -> None:
        """保存当前配置到文件"""
        try:
            with open(self.config_path, "wb") as f:
                f.write(
                    orjson.dumps(
                        self._config, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
                    )
                )
        except (OSError, IOError) as e:
            logger.error("保存配置失败: {}", e)

    def get(self, key_path: str, default=None) -> Any:
        """通过点分隔的路径获取配置值
        Args:
            key_path (str): 配置路径，例如 "app.theme"
            default (Any, optional): 默认值，如果路径不存在则返回。 Defaults to None.
        Returns:
            Any: 配置值或默认值
        Raises:
            ValueError: 如果路径包含空字符串或空格
        """
        keys = key_path.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def set(self, key_path: str, value: Any) -> None:
        """设置配置值，自动创建中间字典，并保存文件。
        Args:
            key_path (str): 配置路径，例如 "app.theme"
            value (Any): 要设置的值
        Raises:
            ValueError: 如果路径包含空字符串或空格
        """
        keys = key_path.split(".")
        target = self._config
        for k in keys[:-1]:
            if k not in target or not isinstance(target[k], dict):
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        self.save()
        logger.info("设置配置值: {} = {}", key_path, value)

    def reload(self) -> None:
        """重新从文件加载配置（丢失未保存的更改）"""
        self.load()

    @property
    def all(self) -> Dict[str, Any] | None:
        """返回整个配置字典（只读副本）
        Returns:
            Dict[str, Any]: 配置字典的副本，或 None 如果配置字典为空
        Raises:
            ValueError: 如果配置字典为空
        """
        return self._config.copy()
