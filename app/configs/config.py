import os
from pathlib import Path

from app.configs.config_helpers import IntConfigKey, StrConfigKey, load_env_from_yaml_file

env_file_name = os.getenv("ENV_FILE_NAME", "env.yaml")
PROJECT_HOME = Path(__file__).absolute().parent.parent.parent
load_env_from_yaml_file(str(PROJECT_HOME.joinpath(env_file_name)))

# session query timeout
SQLALCHEMY_GLOBAL_QUERY_TIMEOUT = IntConfigKey(
    env_key="SQLALCHEMY_GLOBAL_QUERY_TIMEOUT", default=10
).to_value()


# 连接数据库的URI地址
SQLALCHEMY_DATABASE_URI = StrConfigKey(
    env_key="SQLALCHEMY_DATABASE_URI").to_value()


# 连接数据库的URI地址 读
READ_DATABASE_URI = StrConfigKey(
    env_key="READ_DATABASE_URI").to_value()


# 连接数据库的URI地址 写
WRITE_DATABASE_URI = StrConfigKey(
    env_key="WRITE_DATABASE_URI").to_value()

# Celery 异步任务 连接 rabbitmq 的URI地址
CELERY_BROKER_URL = StrConfigKey(
    env_key="CELERY_BROKER_URL").to_value()
