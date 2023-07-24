from flask import Blueprint

from app.base import app
from app.blueprints.api import blueprint as api_bp
from app.blueprints.api import *

__all__ = ["ping_handlers"]


# 定义蓝图
root = Blueprint("root", __name__)


@root.route("/", methods=["GET", "HEAD"])
def root_head_ping():
    return "ok"


app.register_blueprint(root, url_prefix="/root")
app.register_blueprint(api_bp.api, url_prefix="/api")
