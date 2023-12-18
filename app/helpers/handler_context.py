from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app.models.user.user import User
from app.base import redis


class HandlerContext:

    @staticmethod
    def success(data=None, message=None, status_code=200):
        if isinstance(data, list):
            data = [item.to_dict() if hasattr(item, 'to_dict')
                    else item for item in data]
        elif hasattr(data, 'to_dict'):
            data = data.to_dict()

        response = {
            'message': message if message else 'Success',
            'data': data
        }
        return jsonify(response), status_code

    @staticmethod
    def custom_jwt_required(fn):

        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            if redis.zscore('revoked_tokens', request.headers.get('Authorization')):
                return jsonify({"data": "重新登录"}), 200
            # 在 jwt_required() 内部获取用户标识
            current_user_id = get_jwt_identity()
            # 根据用户标识查询用户信息
            request.current_user = User.query.get(current_user_id)
            # 继续执行被装饰的函数
            return fn(*args, **kwargs)

        return wrapper
