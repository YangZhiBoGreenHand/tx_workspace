import time
from flask import jsonify, request
from .blueprint import api
from app.models.user.user import User
from app.base import db, redis
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.helpers.handler_context import HandlerContext as context
from app.base import app


@api.route('/register', methods=['POST'])
def register():
    # 处理注册表单提交
    phone_number = request.form['phone_number']
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    email = request.form['email']
    name = request.form['name']
    if not phone_number or not password1 or not password2 or not email:
        return jsonify({'error': '请输入用户名和密码'}), 400
    if password1 != password2:
        return jsonify({'error': '两次输入的密码不一致'}), 400
    # 检查用户名是否已经存在
    existing_user = User.query.filter_by(phone_number=phone_number).first()
    if existing_user:
        return jsonify({'error': '该用户名已被注册'}), 400
    user = User(phone_number=phone_number, name=name, email=email)
    user.set_password(password1)
    db.session.add(user)
    db.session.commit()
    return jsonify({'data': '注册成功'}), 200


@api.route('/login', methods=['POST'])
def login():
    print(111111111)
    # 处理登录表单提交
    phone_number = request.json['phone_number']
    password = request.json['password']
    user = User.query.filter_by(phone_number=phone_number).first()
    if user and user.check_password(password):
        # 用户名和密码匹配，登录成功
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        # 用户名或密码不匹配，登录失败
        return jsonify({'data': '登录失败。请检查用户名和密码。'}), 200


@api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # 刷新访问令牌
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=new_access_token), 200


@api.route('/logout', methods=['POST'])
@context.custom_jwt_required
def logout():
    # 获取当前用户的身份信息
    authorization_header = request.headers.get('Authorization')

    redis.zadd('revoked_tokens', {authorization_header: time.time()})
    revoked_tokens_count = redis.zcard('revoked_tokens')
    MAX_REVOKED_TOKENS = app.config["MAX_REVOKED_TOKENS"]
    if revoked_tokens_count > MAX_REVOKED_TOKENS:
        redis.zremrangebyrank('revoked_tokens', 0,
                              revoked_tokens_count - MAX_REVOKED_TOKENS - 1)

    # 返回响应
    return jsonify({"data": "登出成功"}), 200
