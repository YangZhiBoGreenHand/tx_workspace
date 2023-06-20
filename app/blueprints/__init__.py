from flask import Blueprint

from app.base import app

__all__ = ["ping_handlers"]


# 定义蓝图
root = Blueprint("root", __name__)


@root.route("/", methods=["GET", "HEAD"])
def root_head_ping():
    return "ok"


app.register_blueprint(root, url_prefix="/root")
