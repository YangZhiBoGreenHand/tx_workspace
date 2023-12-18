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


# OPENAI 大模型的私密 KEY
OPENAI_API_KEY = StrConfigKey(
    env_key="OPENAI_API_KEY").to_value()


# JWT_SECRET_KEY
JWT_SECRET_KEY = StrConfigKey(
    env_key="JWT_SECRET_KEY").to_value()

# JWT_SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = IntConfigKey(
    env_key="JWT_ACCESS_TOKEN_EXPIRES").to_value()

# JWT_SECRET_KEY
JWT_REFRESH_TOKEN_EXPIRES = IntConfigKey(
    env_key="JWT_ACCESS_TOKEN_EXPIRES").to_value()

# REDIS_URL
REDIS_URL = StrConfigKey(
    env_key="REDIS_URL").to_value()

# MAX_REVOKED_TOKENS
MAX_REVOKED_TOKENS = IntConfigKey(
    env_key="MAX_REVOKED_TOKENS").to_value()
