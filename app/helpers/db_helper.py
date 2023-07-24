from flask import Flask, g, has_app_context
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from functools import wraps


_ATTR_SESSION_TYPE = "_db_type"


def mark_readonly(session_type='mark_readonly'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            setattr(g, _ATTR_SESSION_TYPE, session_type)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def mark_readwrite(session_type='mark_readwrite'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            setattr(g, _ATTR_SESSION_TYPE, session_type)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class MySQLAlchemy(SQLAlchemy):

    def __init__(self, app: Flask = None, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.read_engine = create_engine(app.config['READ_DATABASE_URI'])
        self.write_engine = create_engine(app.config['WRITE_DATABASE_URI'])
        # 使用 这个 scoped_session 对象会自动管理 session 会话，也就是自动释放
        self.ReadSession = scoped_session(sessionmaker(bind=self.read_engine))
        self.WriteSession = scoped_session(
            sessionmaker(bind=self.write_engine))

    @property
    def session(self):
        """获取当前读写设置下的 session"""
        if has_app_context():
            db_type = getattr(g, _ATTR_SESSION_TYPE, 'default')
            if db_type == 'mark_readonly':
                return self.ReadSession
            if db_type == 'mark_readwrite':
                return self.WriteSession
        return self._session

    @session.setter
    def session(self, value):
        """设置 session 属性"""
        self._session = value
