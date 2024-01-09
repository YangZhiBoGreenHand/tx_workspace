from elasticapm.contrib.flask import ElasticAPM
from app.configs import config
from app.configs.config import (
    SQLALCHEMY_GLOBAL_QUERY_TIMEOUT,
)
from flask import Flask
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_jwt_extended import JWTManager
from elasticapm.contrib.flask import ElasticAPM
import logging

app = Flask(__name__)
print("app created")
app.logger.setLevel(logging.DEBUG)

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


# Or use ELASTIC_APM in your application's settings
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'yzb_server',
    'SECRET_TOKEN': '',
    'SERVER_URL': 'http://localhost:8200',
    'ENVIRONMENT': 'dev',
    'DEBUG': True
}

apm = ElasticAPM(app)
