import json
import logging
import os
from collections import UserString
from typing import Any, List, Union, cast

import yaml


def load_env_from_yaml_file(yaml_file="./env.yaml"):
    """读取yaml文件放到环境变量"""
    if not os.path.exists(yaml_file):
        logging.warning("%s 配置文件不存在", yaml_file)
        return

    file_path = os.path.abspath(yaml_file)
    logging.info("Read config from %s", file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        d = cast(Any, yaml.safe_load(f))
        for k, v in d.items():
            sv: str
            if isinstance(v, (list, dict, tuple)):
                sv = json.dumps(v)
            else:
                sv = str(v)
            os.environ[str(k)] = sv


class ConfigKey(UserString):
    def __init__(
        self,
        require: bool = True,
        require_deploy_type: List[str] = None,
        default: Union[str, int, float] = "",
        env_key: str = "",
        comment: str = "",
        choice: list = None,
        empty_warning: bool = False,
    ):
        """配置项, 默认都是字符串, 可以用 to_str, to_int 进行类型转换

        :param require: 是否必填
        :param require_deploy_type: 必填的环境
        :param default: 默认值
        :param env_key: 从环境变量获取的key
        :param comment: 配置说明
        :param empty_warning: 为空是否logging.warn
        """
        if isinstance(default, (int, float)):
            default = str(default)
        elif isinstance(default, str):
            default = default
        else:
            raise TypeError("配置默认值必须为字符串或整型")

        self.require = require
        self.default = default
        self.env_key = env_key
        self.comment = comment

        value = ""
        if env_key:
            value = os.getenv(env_key, "")
        if not value:
            if default:
                value = default
                if env_key:
                    os.environ[env_key] = default
            if require and not value:
                DEPLOY_TYPE = os.getenv("DEPLOY_TYPE")
                if (not require_deploy_type) or (DEPLOY_TYPE in require_deploy_type):
                    raise ValueError(
                        f"运行环境为 {DEPLOY_TYPE} 时, 配置 {env_key} 不能为空")
        if value and choice:
            if value not in choice:
                raise TypeError(f"配置项必须是 {choice} 中的一个")

        self.value = value

        if not value and empty_warning:
            logging.warning(f"配置 {env_key} 为空")

        super(ConfigKey, self).__init__(value)

    def to_str(self) -> str:
        return self.value

    def to_int(self) -> int:
        return int(self.value or 0)


class StrConfigKey(ConfigKey):
    def to_value(self) -> str:
        return self.to_str()


class IntConfigKey(ConfigKey):
    def to_value(self) -> int:
        return self.to_int()


class BoolConfigKey(ConfigKey):
    def to_value(self) -> bool:
        return self.to_str().lower() in ["on", "open", "1", "true"]
