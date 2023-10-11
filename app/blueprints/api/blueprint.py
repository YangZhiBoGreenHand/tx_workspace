
from flask import Blueprint, jsonify
from app.base import app, db

api = Blueprint("api", __name__)


@app.errorhandler(Exception)
def handle_exception(e):
    db.session.rollback()
    # 可以区分不同的异常，进行不同的处理
    if isinstance(e, ValueError):
        response = jsonify(message=str(e))
        response.status_code = 400
        return response

    # 对于不可预知的错误，可以返回一个通用的500响应
    response = jsonify(message="Internal Server Error")
    response.status_code = 500
    return response
