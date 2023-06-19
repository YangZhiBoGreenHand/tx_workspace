from app.configs import config
from app.configs.config import (
    SQLALCHEMY_GLOBAL_QUERY_TIMEOUT,
)
from flask import Flask
app = Flask(__name__)
print("app created")

# 加载配置变量
for key in dir(config):
    if key not in [
        "__builtins__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__spec__",
    ]:
        app.config[key] = getattr(config, key)


def create_sqlalchemy_app():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(
        app.config["SQLALCHEMY_DATABASE_URI"],
        connect_args={"options": f"-c statement_timeout={SQLALCHEMY_GLOBAL_QUERY_TIMEOUT * 1000}"})
    _db = sessionmaker(bind=engine)
    return _db


db = create_sqlalchemy_app()
print("db ready")
