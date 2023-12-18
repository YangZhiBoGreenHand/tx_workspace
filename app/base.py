from app.configs import config
from app.configs.config import (
    SQLALCHEMY_GLOBAL_QUERY_TIMEOUT,
)
from flask import Flask
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_jwt_extended import JWTManager

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
    from app.helpers.db_helper import MySQLAlchemy
    _db = MySQLAlchemy(app)

    return _db


db = create_sqlalchemy_app()

print("db ready")


def migrate_db():
    from app.models import __init__
    Migrate(app, db)


migrate_db()
print("migrate ready")

redis = FlaskRedis(app)
print("redis ready")

jwt = JWTManager(app)
print("jwt ready")
